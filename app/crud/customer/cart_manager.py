from ...utils.timezone import ist_now
from ...db.base.database_manager import DatabaseManager
from ...models.customer.cart_model import Cart, CartItem
from ...models.customer.medicine_model import Medicine
from ...schemas.customer.cart_schema import AddToCart, UpdateCartItem
from ...utils.logger import get_logger

logger = get_logger(__name__)


class CartManager:
    def __init__(self, db_type: str):
        self.db = DatabaseManager(db_type)

    # -------------------------------------------------------------
    # Ensure cart exists
    # -------------------------------------------------------------
    async def _get_or_create_cart(self, customer_id: int):
        cart = await self.db.read(Cart, {"CustomerId": customer_id})

        # DatabaseManager.read() returns a list of results.
        # when we expect a single row, take the first element if present.
        if cart:
            return cart[0].CartId

        await self.db.create(
            Cart,
            {
                "CustomerId": customer_id,
                "CreatedAt": ist_now()
            }
        )

        cart = await self.db.read(Cart, {"CustomerId": customer_id})
        return cart[0].CartId

    # -------------------------------------------------------------
    # Add item to cart (Amazon-style)
    # -------------------------------------------------------------
    async def add_to_cart(self, data: AddToCart):
        try:
            await self.db.connect()

            cart_id = await self._get_or_create_cart(data.CustomerId)

            # fetch medicine for getting current price
            medicine = await self.db.read(Medicine, {"MedicineId": data.MedicineId})
            # read() returns a list even for single-object queries
            if not medicine:
                return {"success": False, "message": "Medicine not found"}

            med = medicine[0]

            existing = await self.db.read(CartItem, {"CartId": cart_id, "MedicineId": data.MedicineId})

            if existing:
                # take the first item when expecting a single row
                existing_item = existing[0]
                new_qty = existing_item.Quantity + data.Quantity
                await self.db.update(
                    CartItem,
                    {"CartItemId": existing_item.CartItemId},
                    {"Quantity": new_qty}
                )
                return {"success": True, "message": "Cart updated"}

            # Store price for comparison later
            await self.db.create(
                CartItem,
                {
                    "CartId": cart_id,
                    "MedicineId": data.MedicineId,
                    "Quantity": data.Quantity,
                    "StoredPrice": med.UnitPrice
                }
            )
            return {"success": True, "message": "Item added to cart"}

        except Exception as e:
            logger.error(f"Add to cart error: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db.disconnect()

    # -------------------------------------------------------------
    # Get enriched cart with Amazon-style price tracking
    # -------------------------------------------------------------
    async def get_cart(self, customer_id: int):
        try:
            await self.db.connect()

            cart = await self.db.read(Cart, {"CustomerId": customer_id})

            if not cart:
                return {
                    "CartId": None,
                    "CustomerId": customer_id,
                    "Items": [],
                    "TotalAmount": 0
                }
            # cart is a list -> take the first element
            cart_obj = cart[0]

            cart_items = await self.db.read(CartItem, {"CartId": cart_obj.CartId})

            enriched_list = []
            total = 0

            for item in cart_items:
                med = await self.db.read(Medicine, {"MedicineId": item.MedicineId})
                if not med:
                    continue
                med_obj = med[0]

                old_price = item.StoredPrice
                new_price = med_obj.UnitPrice

                price_changed = (old_price != new_price)

                amount = new_price * item.Quantity
                total += amount

                enriched_list.append({
                    "CartItemId": item.CartItemId,
                    "MedicineId": med_obj.MedicineId,
                    "Name": med_obj.Name,
                    "ImgUrl": med_obj.ImgUrl,
                    "OldPrice": old_price,
                    "NewPrice": new_price,
                    "PriceChanged": price_changed,
                    "Quantity": item.Quantity,
                    "Amount": amount
                })

            return {
                "CartId": cart_obj.CartId,
                "CustomerId": customer_id,
                "Items": enriched_list,
                "TotalAmount": total
            }

        except Exception as e:
            logger.error(f"Get cart error: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db.disconnect()

    # -------------------------------------------------------------
    # Update quantity only
    # -------------------------------------------------------------
    async def update_item(self, cart_item_id: int, data: UpdateCartItem):
        try:
            await self.db.connect()

            updated = await self.db.update(
                CartItem,
                {"CartItemId": cart_item_id},
                data.dict(exclude_unset=True)
            )

            if updated:
                return {"success": True, "message": "Item updated"}

            return {"success": False, "message": "Item not found"}

        except Exception as e:
            logger.error(f"Update item error: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db.disconnect()

    # -------------------------------------------------------------
    # Remove an item
    # -------------------------------------------------------------
    async def delete_item(self, cart_item_id: int):
        try:
            await self.db.connect()

            deleted = await self.db.delete(CartItem, {"CartItemId": cart_item_id})

            if deleted:
                return {"success": True, "message": "Item deleted"}

            return {"success": False, "message": "Item not found"}

        except Exception as e:
            logger.error(f"Delete cart item error: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db.disconnect()

    # -------------------------------------------------------------
    # Clear cart
    # -------------------------------------------------------------
    async def clear_cart(self, customer_id: int):
        try:
            await self.db.connect()

            cart = await self.db.read(Cart, {"CustomerId": customer_id})
            if not cart:
                return {"success": True, "message": "Cart is empty"}
            removed = await self.db.delete(CartItem, {"CartId": cart[0].CartId})

            return {"success": True, "message": f"{removed} items removed"}

        except Exception as e:
            logger.error(f"Clear cart error: {e}")
            return {"success": False, "message": str(e)}

        finally:
            await self.db.disconnect()
