use retail_dashboard

db.campaign_feedback.insertMany([
  {
    campaign_id: "CMP-2025-001",
    campaign_name: "New Year Electronics Sale",
    product: "Wireless Mouse",
    category: "Electronics",
    region: "South",
    store_id: 1,
    discount_percent: 5,
    start_date: new Date("2025-01-01"),
    end_date: new Date("2025-01-15"),
    feedback: [
      { customer: "Customer A", comment: "Good price, fast checkout.", rating: 4 },
      { customer: "Customer B", comment: "Stock ran out too quickly.", rating: 3 }
    ],
    avg_rating: 3.5,
    created_at: new Date("2025-01-16")
  },
  {
    campaign_id: "CMP-2025-002",
    campaign_name: "Winter Apparel Clearance",
    product: "Cotton T-Shirt",
    category: "Apparel",
    region: "West",
    store_id: 4,
    discount_percent: 20,
    start_date: new Date("2025-01-05"),
    end_date: new Date("2025-01-20"),
    feedback: [
      { customer: "Customer C", comment: "Great discount, limited sizes.", rating: 4 },
      { customer: "Customer D", comment: "Quality is good for the price.", rating: 5 }
    ],
    avg_rating: 4.5,
    created_at: new Date("2025-01-21")
  },
  {
    campaign_id: "CMP-2025-003",
    campaign_name: "Footwear Fest",
    product: "Running Shoes",
    category: "Footwear",
    region: "South",
    store_id: 3,
    discount_percent: 5,
    start_date: new Date("2025-01-03"),
    end_date: new Date("2025-01-18"),
    feedback: [
      { customer: "Customer E", comment: "Discount too small, returned the pair.", rating: 2 }
    ],
    avg_rating: 2,
    created_at: new Date("2025-01-19")
  }
])
