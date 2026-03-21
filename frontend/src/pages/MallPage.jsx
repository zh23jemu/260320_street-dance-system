import { useEffect, useState } from 'react'

import { apiFetch } from '../api'

const initialProduct = {
  name: '',
  category: '',
  price: '',
  stock: '',
  description: '',
}

function MallPage({ currentUser, setNotice }) {
  const [products, setProducts] = useState([])
  const [cart, setCart] = useState([])
  const [orders, setOrders] = useState([])
  const [form, setForm] = useState(initialProduct)

  async function loadProducts() {
    try {
      const data = await apiFetch('/mall/products/')
      setProducts(data.items)
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function loadPrivateData() {
    if (!currentUser) {
      setCart([])
      setOrders([])
      return
    }

    try {
      const [cartData, ordersData] = await Promise.all([
        apiFetch('/mall/cart/'),
        apiFetch('/mall/orders/'),
      ])
      setCart(cartData.items)
      setOrders(ordersData.items)
    } catch (error) {
      setNotice(error.message)
    }
  }

  useEffect(() => {
    loadProducts()
  }, [])

  useEffect(() => {
    loadPrivateData()
  }, [currentUser])

  async function createProduct(event) {
    event.preventDefault()
    try {
      await apiFetch('/mall/products/', {
        method: 'POST',
        body: JSON.stringify({
          ...form,
          price: Number(form.price),
          stock: Number(form.stock),
        }),
      })
      setNotice('商品创建成功')
      setForm(initialProduct)
      await loadProducts()
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function addToCart(productId) {
    try {
      await apiFetch('/mall/cart/', {
        method: 'POST',
        body: JSON.stringify({ product_id: productId, quantity: 1 }),
      })
      setNotice('已加入购物车')
      await loadPrivateData()
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function createOrder() {
    try {
      await apiFetch('/mall/orders/create/', { method: 'POST', body: JSON.stringify({}) })
      setNotice('订单已创建')
      await Promise.all([loadProducts(), loadPrivateData()])
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function payOrder(orderId) {
    try {
      await apiFetch(`/mall/orders/${orderId}/pay/`, { method: 'POST', body: JSON.stringify({}) })
      setNotice('模拟支付成功')
      await loadPrivateData()
    } catch (error) {
      setNotice(error.message)
    }
  }

  return (
    <div className="page-grid">
      <section className="panel-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Street Shop</p>
            <h2>舞蹈服饰与装备</h2>
          </div>
          <span>{products.length} 件商品</span>
        </div>

        <div className="product-grid">
          {products.map((product) => (
            <article key={product.id} className="activity-card">
              <div className="stack-item">
                <strong>{product.name}</strong>
                <span>{product.category}</span>
                <small>{product.description || '暂无描述'}</small>
              </div>
              <div className="mini-row">
                <strong>¥ {product.price}</strong>
                <span>库存 {product.stock}</span>
              </div>
              <button onClick={() => addToCart(product.id)}>加入购物车</button>
            </article>
          ))}
        </div>
      </section>

      <section className="triple-grid">
        <article className="panel-card">
          <div className="section-heading">
            <h2>新增商品</h2>
          </div>
          <form className="form-grid" onSubmit={createProduct}>
            <input placeholder="商品名称" value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} />
            <input placeholder="分类" value={form.category} onChange={(event) => setForm({ ...form, category: event.target.value })} />
            <input placeholder="价格" value={form.price} onChange={(event) => setForm({ ...form, price: event.target.value })} />
            <input placeholder="库存" value={form.stock} onChange={(event) => setForm({ ...form, stock: event.target.value })} />
            <textarea placeholder="描述" value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} />
            <button type="submit">发布商品</button>
          </form>
        </article>

        <article className="panel-card">
          <div className="section-heading">
            <h2>购物车</h2>
            <button onClick={createOrder}>创建订单</button>
          </div>
          <div className="scroll-list fixed-height">
            {cart.map((item) => (
              <div key={item.id} className="list-card static-card">
                <strong>{item.product.name}</strong>
                <span>数量 {item.quantity}</span>
                <small>小计 ¥ {item.subtotal}</small>
              </div>
            ))}
          </div>
        </article>

        <article className="panel-card">
          <div className="section-heading">
            <h2>订单记录</h2>
          </div>
          <div className="scroll-list fixed-height">
            {orders.map((order) => (
              <div key={order.id} className="list-card static-card">
                <strong>订单 #{order.id}</strong>
                <span>{order.order_status}</span>
                <small>金额 ¥ {order.total_amount}</small>
                {!order.payment_status ? (
                  <button onClick={() => payOrder(order.id)}>立即支付</button>
                ) : (
                  <small>已支付</small>
                )}
              </div>
            ))}
          </div>
        </article>
      </section>
    </div>
  )
}

export default MallPage
