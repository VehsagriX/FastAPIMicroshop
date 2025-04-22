import asyncio


from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from core.models import (
    db_helper,
    User,
    Product,
    Post,
    Profile,
    Order,
    OrderProductRelation,
)


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(name=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stm = select(User).where(User.name == username)
    # result: Result = await session.execute(stm)
    # user: User | None = result.scalar_one_or_none()
    user: User | None = await session.scalar(stm)
    print("found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str,
    last_name: str,
) -> Profile:
    profile = Profile(
        user_id=user_id,  # type: ignore
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()

    return profile


async def show_users_with_profiles(session: AsyncSession):
    stm = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result:Result = await session.execute(stm)
    # users = result.scalars()
    users = await session.scalars(stm)
    users_list = []
    for user in users:
        users_list.append(user)
        print(user)
        print(user.profile.first_name)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_title: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_title]
    session.add_all(posts)
    await session.commit()
    print("posts", posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print("*" * 10)
        print(user)
        for posts in user.posts:
            print("-", posts)


async def get_post_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:
        print("post", post)
        print("author", post.user)


async def get_users_with_posts_and_profiles(session: AsyncSession):
    stmt = (
        select(User)
        .options(joinedload(User.profile), selectinload(User.posts))
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    for user in users:
        print("*" * 10)
        print(user, user.profile and user.profile.first_name)
        for posts in user.posts:
            print("-", posts)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(joinedload(Profile.user).selectinload(User.posts))
        .where(User.name == "JHON")
        .order_by(Profile.user_id)
    )

    profiles = await session.scalars(stmt)
    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def main_to_relation(session: AsyncSession):
    await create_user(session=session, username="alice")
    user_jhon = await get_user_by_username(session=session, username="JHON")
    await get_user_by_username(session=session, username="BOB")
    user_sam = await get_user_by_username(session=session, username="Sam")
    await create_user_profile(
        session=session,
        user_id=user_jhon.id,  # type: ignore
        first_name="JHON",
        last_name="SMIT",
    )
    await create_user_profile(
        session=session,
        user_id=user_sam.id,  # type: ignore
        first_name="SAM",
        last_name="WHITE",
    )
    await show_users_with_profiles(session=session)
    await create_posts(session, user_jhon.id, "SQLA 20", "SQLA Joins")
    await create_posts(
        session, user_sam.id, "XSAWQ12", "213SADASZAS ASDAS", "more learn FastApi"
    )
    await get_users_with_posts(session=session)
    await get_post_with_authors(session)
    await get_users_with_posts_and_profiles(session)
    await get_profiles_with_users_and_users_with_posts(session)


async def create_order(
    session: AsyncSession,
    promocode: str | None = None,
) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession,
    name: str,
    description: str,
    price: int,
) -> Product:
    product = Product(name=name, description=description, price=price)
    session.add(product)
    await session.commit()
    return product


async def create_orders_and_products(session: AsyncSession):
    order_1 = await create_order(session=session)
    order_2 = await create_order(session=session, promocode="promo")

    mouse = await create_product(
        session=session,
        name="Mouse Logitach",
        description="MT 750S",
        price=150,
    )
    keyboard = await create_product(
        session=session,
        name="Keyboard Logitech",
        description="K220",
        price=250,
    )
    display = await create_product(
        session=session,
        name="Display Xiaomi",
        description="24/12",
        price=450,
    )

    order_1 = await session.scalar(
        select(Order)
        .where(Order.id == order_1.id)
        .options(
            selectinload(Order.products),
        )
    )
    order_2 = await session.scalar(
        select(Order)
        .where(Order.id == order_2.id)
        .options(
            selectinload(Order.products),
        ),
    )

    order_1.products.append(mouse)
    order_1.products.append(keyboard)

    order_2.products.append(keyboard)
    order_2.products.append(display)

    await session.commit()


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = select(Order).options(selectinload(Order.products)).order_by(Order.id)
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session=session)
    for order in orders:
        print(
            order.id,
            order.promocode,
            order.created_at,
            "products: ",
        )
        for products in order.products:
            print("-", products.name, products.description, products.price)


async def get_orders_with_products_assoc(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductRelation.product
            )
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_get_orders_with_products_with_associations(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session=session)

    for order in orders:
        print(
            order.id,
            order.promocode,
            order.created_at,
            "products: ",
        )
        for (
            order_product_details
        ) in order.products_details:  # type: OrderProductRelation
            print(
                "-",
                order_product_details.product.id,
                order_product_details.product.name,
                order_product_details.product.description,
                order_product_details.product.price,
                "qty: ",
                order_product_details.count,
            )


async def create_gift_product_for_existings_orders(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session=session)
    gift_product = await create_product(
        session=session,
        name="Gift",
        description="Gift for u",
        price=0,
    )
    for order in orders:
        order.products_details.append(
            OrderProductRelation(
                count=1,
                unit_price=0,
                product=gift_product,
            )
        )

    await session.commit()


async def demo_m2m(session: AsyncSession):
    # await demo_get_orders_with_products_through_secondary
    await demo_get_orders_with_products_with_associations(session=session)


async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session=session)


if __name__ == "__main__":
    asyncio.run(main())
