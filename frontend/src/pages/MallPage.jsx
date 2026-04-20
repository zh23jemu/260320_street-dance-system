import { useEffect, useState } from 'react'

import { apiFetch } from '../api'

const initialProduct = {
  name: '',
  category: '',
  price: '',
  stock: '',
  description: '',
}

// 商城页需要让用户一进入页面就能开始“选东西”，因此这里准备一组前端样品。
// 当后端暂无商品数据时，页面会展示这些样品，并允许用户先加入试选清单；
// 如果后端已经有真实商品，则优先展示真实商品，真实商品仍然走购物车和订单接口。
const sampleProducts = [
  {
    id: 'sample-hoodie',
    name: '城市练舞宽松卫衣',
    category: '服装',
    price: '199.00',
    stock: 24,
    description: '适合日常练舞和排练穿搭，宽松版型便于完成大幅度动作。',
    sample: true,
  },
  {
    id: 'sample-pants',
    name: '地板动作训练长裤',
    category: '服装',
    price: '169.00',
    stock: 18,
    description: '耐磨面料，适合Breaking、Popping等训练场景。',
    sample: true,
  },
  {
    id: 'sample-cap',
    name: '演出鸭舌帽',
    category: '配件',
    price: '89.00',
    stock: 36,
    description: '基础百搭款，可用于舞台造型、街拍和日常练习。',
    sample: true,
  },
  {
    id: 'sample-kneepad',
    name: '膝部防护护具',
    category: '护具',
    price: '59.00',
    stock: 42,
    description: '为地板动作训练提供基础缓冲保护，适合新手练习。',
    sample: true,
  },
]

function MallPage({ currentUser, setNotice }) {
  const [products, setProducts] = useState([])
  const [cart, setCart] = useState([])
  const [orders, setOrders] = useState([])
  const [sampleSelection, setSampleSelection] = useState([])
  const [form, setForm] = useState(initialProduct)
  const displayProducts = products.length > 0 ? products : sampleProducts
  const hasRealProducts = products.length > 0

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

  function toggleSampleSelection(product) {
    setSampleSelection((current) => {
      const exists = current.some((item) => item.id === product.id)
      if (exists) {
        setNotice('已从试选清单移除')
        return current.filter((item) => item.id !== product.id)
      }

      setNotice('已加入试选清单')
      return [...current, product]
    })
  }

  function handleProductAction(product) {
    if (product.sample) {
      toggleSampleSelection(product)
      return
    }

    addToCart(product.id)
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
      <section className="shop-hero">
        <div>
          <p className="eyebrow">Street Shop</p>
          <h2>先挑装备，再去舞池。</h2>
          <p>商城页优先展示可选商品。没有后端商品时，会先展示样品区，让用户可以直接试选卫衣、训练裤、配件和护具。</p>
        </div>
        <div className="shop-hero-actions">
          <strong>{displayProducts.length} 件可选商品</strong>
          <span>{hasRealProducts ? '当前为真实商品，可加入购物车' : '当前为样品展示，可加入试选清单'}</span>
        </div>
      </section>

      <section className="panel-card shop-product-panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Pick First</p>
            <h2>舞蹈服饰与装备</h2>
          </div>
          <span>{hasRealProducts ? '购物车模式' : '样品试选模式'}</span>
        </div>

        <div className="product-grid">
          {displayProducts.map((product) => {
            const selected = sampleSelection.some((item) => item.id === product.id)
            return (
            <article key={product.id} className={`activity-card product-card ${selected ? 'selected-product' : ''}`}>
              <div className="activity-meta">
                <span>{product.category}</span>
                <span>{product.sample ? '样品' : product.status}</span>
              </div>
              <div className="stack-item">
                <strong>{product.name}</strong>
                <small>{product.description || '暂无描述'}</small>
              </div>
              <div className="mini-row">
                <strong>¥ {product.price}</strong>
                <span>库存 {product.stock}</span>
              </div>
              <button onClick={() => handleProductAction(product)}>
                {product.sample ? (selected ? '取消试选' : '加入试选清单') : '加入购物车'}
              </button>
            </article>
            )
          })}
        </div>
      </section>

      <section className="triple-grid">
        {!hasRealProducts ? (
          <article className="panel-card">
            <div className="section-heading">
              <h2>试选清单</h2>
              <span>{sampleSelection.length} 件</span>
            </div>
            <div className="scroll-list fixed-height">
              {sampleSelection.length === 0 ? (
                <div className="list-card static-card">
                  <strong>还没有选择样品</strong>
                  <small>点击上方商品卡片即可先把喜欢的装备加入试选清单。</small>
                </div>
              ) : (
                sampleSelection.map((item) => (
                  <div key={item.id} className="list-card static-card">
                    <strong>{item.name}</strong>
                    <span>{item.category}</span>
                    <small>参考价 ¥ {item.price}</small>
                  </div>
                ))
              )}
            </div>
          </article>
        ) : null}

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
