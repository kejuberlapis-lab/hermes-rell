// Lamar Coffee — Global State & Shared Architecture

// 1. Menu & Bean Database
const GLOBAL_MENU = [
  {
    id: 1,
    name: "Lamar Aren Macchiato",
    category: "espresso",
    price: 38000,
    notes: "Double ristretto Aceh Gayo, aren nira Kulon Progo, fresh oat milk & sea salt crema.",
    badge: "Chef Signature",
    image: "https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=400&q=80",
    tags: ["Signature", "Dairy-Free Option", "Iced/Hot"]
  },
  {
    id: 2,
    name: "Kyoto 12h Cold Drip",
    category: "manual",
    price: 42000,
    notes: "Single-origin Ethiopia Guji diseduh tetes demi tetes 12 jam. Floral winey & madu.",
    badge: "Slow Drip",
    image: "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=400&q=80",
    tags: ["Manual Brew", "Cold Extraction", "Zero Sugar"]
  },
  {
    id: 3,
    name: "Pistachio Spanish Latte",
    category: "espresso",
    price: 45000,
    notes: "Espresso Toraja Sapan, pasta pistachio murni Sicilia, sweet steamed milk lembut.",
    badge: "Artisan Nut",
    image: "https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?auto=format&fit=crop&w=400&q=80",
    tags: ["Artisan", "Sweet & Rich"]
  },
  {
    id: 4,
    name: "V60 Pour Over Aceh Gayo",
    category: "manual",
    price: 36000,
    notes: "Seduhan manual filter V60 aroma jasmine, bright wild berries, clean aftertaste.",
    badge: "Single Origin",
    image: "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=400&q=80",
    tags: ["Filter V60", "Fruity", "Light Roast"]
  },
  {
    id: 5,
    name: "V60 Toraja Sapan Minanga",
    category: "manual",
    price: 38000,
    notes: "Ketinggian 1.850 mdpl. Notes bergamot, herbal spices & aftertaste manis tebal.",
    badge: "Single Origin",
    image: "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=400&q=80",
    tags: ["Filter V60", "Herbal", "Medium-Light"]
  },
  {
    id: 6,
    name: "Classic Flat White (Double)",
    category: "espresso",
    price: 34000,
    notes: "Double shot ristretto pekat dengan microfoam susu bertekstur sutra halus.",
    badge: "Classic",
    image: "https://images.unsplash.com/photo-1577968897966-3d4325b36b61?auto=format&fit=crop&w=400&q=80",
    tags: ["Classic Espresso", "High Caffeine"]
  },
  {
    id: 7,
    name: "Cascara Rosella Sparkling",
    category: "botanical",
    price: 36000,
    notes: "Kulit ceri kopi kering, seduhan teh bunga rosela merah, lemon segar & soda.",
    badge: "Botanical",
    image: "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=400&q=80",
    tags: ["Low Caffeine", "Refreshing", "Sparkling"]
  },
  {
    id: 8,
    name: "Ceremonial Uji Matcha Latte",
    category: "botanical",
    price: 40000,
    notes: "Bubuk matcha grade seremonial Kyoto, dipadukan susu oat murni hangat/dingin.",
    badge: "Direct Japan",
    image: "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&w=400&q=80",
    tags: ["Superfood", "Kyoto Import"]
  },
  {
    id: 9,
    name: "Artisan Almond Butter Croissant",
    category: "pastry",
    price: 32000,
    notes: "Croissant mentega Prancis berlapis renyah dengan pasta almond panggang.",
    badge: "Fresh Bake",
    image: "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=400&q=80",
    tags: ["Bakery", "Fresh Daily"]
  },
  {
    id: 10,
    name: "Truffle Mushroom Sourdough Toast",
    category: "pastry",
    price: 48000,
    notes: "Roti sourdough panggang, tumis jamur champignon saus krim truffle & telur omega.",
    badge: "Brunch",
    image: "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=400&q=80",
    tags: ["Hot Kitchen", "Savoury Brunch"]
  }
];

const GLOBAL_BEANS = [
  {
    id: 101,
    name: "Aceh Gayo Pantan Musara",
    origin: "Sumatra, Indonesia",
    altitude: "1.600 mdpl",
    process: "Double Anaerobic Natural",
    score: "88.5",
    tastingNotes: "Wild Blueberry, Dark Cherry, Brown Sugar, Mint",
    roastProfile: "Filter / Light-Medium",
    price200g: 120000,
    price500g: 275000,
    price1kg: 510000,
    image: "https://images.unsplash.com/photo-1587734195503-904fca47e0e9?auto=format&fit=crop&w=400&q=80"
  },
  {
    id: 102,
    name: "Toraja Sapan Minanga",
    origin: "Sulawesi, Indonesia",
    altitude: "1.850 mdpl",
    process: "Fully Washed Clean",
    score: "87.7",
    tastingNotes: "Bergamot Tea, Sweet Lemon, Clove, Honey Finish",
    roastProfile: "Filter / Medium-Light",
    price200g: 135000,
    price500g: 310000,
    price1kg: 580000,
    image: "https://images.unsplash.com/photo-1559525839-b184a4d698c7?auto=format&fit=crop&w=400&q=80"
  },
  {
    id: 103,
    name: "Guji Chelchele Heirloom",
    origin: "Yirgacheffe, Ethiopia",
    altitude: "2.050 mdpl",
    process: "Washed Grade 1",
    score: "89.2",
    tastingNotes: "Jasmine Blossom, White Peach, Earl Grey, Lavender",
    roastProfile: "Nordic Light Roast",
    price200g: 160000,
    price500g: 370000,
    price1kg: 690000,
    image: "https://images.unsplash.com/photo-1611854779393-1b2da9d400fe?auto=format&fit=crop&w=400&q=80"
  },
  {
    id: 104,
    name: "Flores Bajawa Kartika",
    origin: "NTT, Indonesia",
    altitude: "1.550 mdpl",
    process: "Semi-Washed Honey",
    score: "86.8",
    tastingNotes: "Milk Chocolate, Roasted Hazelnut, Caramel Apple",
    roastProfile: "Espresso / Medium Roast",
    price200g: 110000,
    price500g: 250000,
    price1kg: 460000,
    image: "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=400&q=80"
  }
];

// 2. Persistent Cart Management (localStorage)
let cart = JSON.parse(localStorage.getItem('lamar_cart') || '[]');

function saveCart() {
  localStorage.setItem('lamar_cart', JSON.stringify(cart));
  updateCartUI();
}

function quickAdd(name, price, notes) {
  const existing = cart.find(i => i.name === name && i.notes === notes);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ id: Date.now(), name, price, notes, qty: 1 });
  }
  saveCart();
  showToast(`✓ Ditambahkan: ${name}`);
}

function changeQty(id, delta) {
  const item = cart.find(i => i.id === id);
  if (item) {
    item.qty += delta;
    if (item.qty <= 0) cart = cart.filter(i => i.id !== id);
  }
  saveCart();
}

function toggleCart(show) {
  const drawer = document.getElementById('cartDrawer');
  if (!drawer) return;
  if (show) {
    drawer.classList.remove('hidden');
    drawer.classList.add('flex');
  } else {
    drawer.classList.remove('flex');
    drawer.classList.add('hidden');
  }
}

function updateCartUI() {
  const badge = document.getElementById('cartCountBadge');
  const totalQty = cart.reduce((sum, i) => sum + i.qty, 0);
  if (badge) {
    badge.innerText = totalQty;
    if (totalQty > 0) {
      badge.className = "px-1.5 py-0.5 rounded-full bg-teal text-white text-[10px] font-mono font-bold leading-none min-w-[18px] text-center";
    } else {
      badge.className = "px-1.5 py-0.5 rounded-full bg-espresso/15 text-espresso/70 text-[10px] font-mono font-bold leading-none min-w-[18px] text-center";
    }
  } else {
      badge.className = "hidden";
    }
  }

  const list = document.getElementById('cartItemsList');
  if (!list) return;

  if (cart.length === 0) {
    list.innerHTML = `<div class="py-12 text-center text-espresso/40 text-xs font-mono">Keranjang seduhan masih kosong.</div>`;
  } else {
    list.innerHTML = cart.map(item => `
      <div class="p-3 bg-white rounded-xl border border-borderWarm flex items-center justify-between gap-3 text-xs font-mono">
        <div class="min-w-0 flex-1">
          <h4 class="font-bold text-espresso truncate">${item.name}</h4>
          <p class="text-[10px] text-espresso/60 truncate">${item.notes}</p>
          <span class="text-ochre font-semibold">Rp ${(item.price * item.qty).toLocaleString('id-ID')}</span>
        </div>
        <div class="flex items-center gap-1.5 bg-sand p-1 rounded-lg">
          <button onclick="changeQty(${item.id}, -1)" class="w-5 h-5 bg-white rounded text-center text-xs font-bold cursor-pointer">-</button>
          <span class="w-4 text-center font-bold text-xs">${item.qty}</span>
          <button onclick="changeQty(${item.id}, 1)" class="w-5 h-5 bg-white rounded text-center text-xs font-bold cursor-pointer">+</button>
        </div>
      </div>
    `).join('');
  }

  const subtotal = cart.reduce((sum, i) => sum + (i.price * i.qty), 0);
  const tax = subtotal * 0.1;
  const grandTotal = subtotal + tax;

  const subEl = document.getElementById('cartSubtotal');
  const taxEl = document.getElementById('cartTax');
  const totalEl = document.getElementById('cartGrandTotal');

  if (subEl) subEl.innerText = `Rp ${subtotal.toLocaleString('id-ID')}`;
  if (taxEl) taxEl.innerText = `Rp ${tax.toLocaleString('id-ID')}`;
  if (totalEl) totalEl.innerText = `Rp ${grandTotal.toLocaleString('id-ID')}`;
}

function checkoutWhatsApp() {
  if (cart.length === 0) return alert('Keranjang masih kosong!');
  let text = `*PESANAN SEDUHAN - LAMAR COFFEE*\n===============================\n`;
  cart.forEach((item, idx) => {
    text += `${idx + 1}. *${item.name}* (x${item.qty})\n   ↳ _${item.notes}_\n   ↳ Rp ${(item.price * item.qty).toLocaleString('id-ID')}\n`;
  });
  const subtotal = cart.reduce((sum, i) => sum + (i.price * i.qty), 0);
  const tax = subtotal * 0.1;
  const grandTotal = subtotal + tax;

  text += `===============================\nSubtotal: Rp ${subtotal.toLocaleString('id-ID')}\nPB1 (10%): Rp ${tax.toLocaleString('id-ID')}\n*TOTAL PEMBAYARAN: Rp ${grandTotal.toLocaleString('id-ID')}*\n\nMohon diproses untuk pesanan / pengiriman saya. Terima kasih! ☕`;
  window.open(`https://wa.me/6281288885262?text=${encodeURIComponent(text)}`, '_blank');
}

function showToast(msg) {
  let toast = document.getElementById('toastNotification');
  if (!toast) return;
  document.getElementById('toastMessage').innerText = msg;
  toast.classList.remove('hidden');
  toast.classList.add('animate-toast');
  setTimeout(() => {
    toast.classList.add('hidden');
    toast.classList.remove('animate-toast');
  }, 3000);
}

// 3. Ambience Audio Synthesizer
let audioPlaying = false;
let audioCtx = null;
let audioNode = null;


function toggleMobileNav() {
  const nav = document.getElementById('mobileNav');
  if (nav) nav.classList.toggle('hidden');
}

// 4. Customizer Modal Logic
let activeCustomItem = null;
let custTemp = 'Iced (Dingin)';
let custMilk = 'Fresh Milk';
let custMilkExtra = 0;
let custSweet = '100%';
let custExtraShotPrice = 0;
let custQty = 1;

function openCustomizer(itemId) {
  const item = GLOBAL_MENU.find(i => i.id === itemId);
  if (!item) return;
  activeCustomItem = item;
  custQty = 1;
  custMilkExtra = 0;
  custExtraShotPrice = 0;
  custTemp = 'Iced (Dingin)';
  custMilk = 'Fresh Milk';
  custSweet = '100%';

  document.getElementById('custImage').src = item.image;
  document.getElementById('custTitle').innerText = item.name;
  document.getElementById('custBasePrice').innerText = `Rp ${item.price.toLocaleString('id-ID')}`;
  const extraShotEl = document.getElementById('custExtraShot');
  if (extraShotEl) extraShotEl.checked = false;
  document.getElementById('custQtyText').innerText = '1';

  resetCustButtons();
  updateCustTotal();

  const modal = document.getElementById('customizerModal');
  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
  }
}

function closeCustomizer() {
  const modal = document.getElementById('customizerModal');
  if (modal) {
    modal.classList.remove('flex');
    modal.classList.add('hidden');
  }
}

function resetCustButtons() {
  const tempBtns = document.querySelectorAll('.temp-btn');
  if (tempBtns.length >= 2) {
    tempBtns[0].className = "temp-btn p-3 rounded-xl border border-ochre bg-linen text-espresso font-bold flex items-center justify-center gap-2 cursor-pointer";
    tempBtns[1].className = "temp-btn p-3 rounded-xl border border-borderWarm bg-white text-espresso/70 hover:border-ochre flex items-center justify-center gap-2 cursor-pointer";
  }

  const milkBtns = document.querySelectorAll('.milk-btn');
  if (milkBtns.length >= 3) {
    milkBtns[0].className = "milk-btn p-2.5 rounded-xl border border-ochre bg-linen text-espresso font-bold text-center cursor-pointer";
    milkBtns[1].className = "milk-btn p-2.5 rounded-xl border border-borderWarm bg-white text-espresso/70 hover:border-ochre text-center cursor-pointer";
    milkBtns[2].className = "milk-btn p-2.5 rounded-xl border border-borderWarm bg-white text-espresso/70 hover:border-ochre text-center cursor-pointer";
  }

  const sweetBtns = document.querySelectorAll('.sweet-btn');
  if (sweetBtns.length >= 4) {
    sweetBtns[0].className = "sweet-btn p-2 rounded-lg border border-ochre bg-linen text-espresso font-bold text-center cursor-pointer";
    sweetBtns[1].className = "sweet-btn p-2 rounded-lg border border-borderWarm bg-white text-espresso/70 text-center cursor-pointer";
    sweetBtns[2].className = "sweet-btn p-2 rounded-lg border border-borderWarm bg-white text-espresso/70 text-center cursor-pointer";
    sweetBtns[3].className = "sweet-btn p-2 rounded-lg border border-borderWarm bg-white text-espresso/70 text-center cursor-pointer";
  }
}

function setCustTemp(val) {
  custTemp = val;
  const btns = document.querySelectorAll('.temp-btn');
  btns.forEach(b => {
    if (b.innerText.includes(val.split(' ')[0])) {
      b.className = "temp-btn p-3 rounded-xl border border-ochre bg-linen text-espresso font-bold flex items-center justify-center gap-2 cursor-pointer";
    } else {
      b.className = "temp-btn p-3 rounded-xl border border-borderWarm bg-white text-espresso/70 hover:border-ochre flex items-center justify-center gap-2 cursor-pointer";
    }
  });
}

function setCustMilk(val, extra) {
  custMilk = val;
  custMilkExtra = extra;
  const btns = document.querySelectorAll('.milk-btn');
  btns.forEach(b => {
    if (b.innerText.includes(val.split(' ')[0])) {
      b.className = "milk-btn p-2.5 rounded-xl border border-ochre bg-linen text-espresso font-bold text-center cursor-pointer";
    } else {
      b.className = "milk-btn p-2.5 rounded-xl border border-borderWarm bg-white text-espresso/70 hover:border-ochre text-center cursor-pointer";
    }
  });
  updateCustTotal();
}

function setCustSweet(val) {
  custSweet = val;
  const btns = document.querySelectorAll('.sweet-btn');
  btns.forEach(b => {
    if (b.innerText === val) {
      b.className = "sweet-btn p-2 rounded-lg border border-ochre bg-linen text-espresso font-bold text-center cursor-pointer";
    } else {
      b.className = "sweet-btn p-2 rounded-lg border border-borderWarm bg-white text-espresso/70 text-center cursor-pointer";
    }
  });
}

function toggleExtraShot() {
  const el = document.getElementById('custExtraShot');
  custExtraShotPrice = (el && el.checked) ? 8000 : 0;
  updateCustTotal();
}

function changeCustQty(delta) {
  custQty = Math.max(1, custQty + delta);
  document.getElementById('custQtyText').innerText = custQty;
  updateCustTotal();
}

function updateCustTotal() {
  if (!activeCustomItem) return;
  const unitPrice = activeCustomItem.price + custMilkExtra + custExtraShotPrice;
  const total = unitPrice * custQty;
  document.getElementById('custTotalPrice').innerText = `Rp ${total.toLocaleString('id-ID')}`;
}

function submitCustomizer() {
  if (!activeCustomItem) return;
  let notes = `${custTemp}, ${custMilk}, Gula ${custSweet}`;
  if (custExtraShotPrice > 0) notes += ', Extra Shot';
  const unitPrice = activeCustomItem.price + custMilkExtra + custExtraShotPrice;

  for (let i = 0; i < custQty; i++) {
    quickAdd(activeCustomItem.name, unitPrice, notes);
  }
  closeCustomizer();
}

document.addEventListener('DOMContentLoaded', () => {
  updateCartUI();
  if (window.lucide) lucide.createIcons();
});