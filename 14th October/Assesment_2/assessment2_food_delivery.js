//use food_delivery_assessment

db.restaurants.insertMany([
  {
    restaurant_id: 101,
    restaurant_name: "Spice Kitchen",
    city: "Hyderabad",
    cuisine: ["Indian", "Biryani"],
    rating: 4.5,
    active: true,
    contact: {
      phone: "9876543210",
      email: "spice@email.com"
    }
  },
  {
    restaurant_id: 102,
    restaurant_name: "Urban Pizza",
    city: "Mumbai",
    cuisine: ["Italian", "Fast Food"],
    rating: 4.2,
    active: true,
    contact: {
      phone: "9988776655",
      email: "pizza@email.com"
    }
  },
  {
    restaurant_id: 103,
    restaurant_name: "Green Bowl",
    city: "Bangalore",
    cuisine: ["Healthy", "Vegetarian"],
    rating: 4.7,
    active: true,
    contact: {
      phone: "9123456780",
      email: "green@email.com"
    }
  },
  {
    restaurant_id: 104,
    restaurant_name: "Burger Point",
    city: "Hyderabad",
    cuisine: ["Fast Food", "Burgers"],
    rating: 3.9,
    active: false,
    contact: {
      phone: "9000011111",
      email: "burger@email.com"
    }
  },
  {
    restaurant_id: 105,
    restaurant_name: "Asian Wok",
    city: "Delhi",
    cuisine: ["Chinese", "Thai"],
    rating: 4.4,
    active: true,
    contact: {
      phone: "9222233333",
      email: "wok@email.com"
    }
  }
])


db.orders.insertMany([
  {
    order_id: 5001,
    restaurant_id: 101,
    customer_name: "Adil",
    order_date: ISODate("2026-09-01"),
    status: "Delivered",
    items: [
      { name: "Chicken Biryani", quantity: 2, price: 320 },
      { name: "Coke", quantity: 2, price: 60 }
    ],
    delivery: {
      city: "Hyderabad",
      fee: 40
    }
  },
  {
    order_id: 5002,
    restaurant_id: 102,
    customer_name: "Megha",
    order_date: ISODate("2026-09-02"),
    status: "Processing",
    items: [
      { name: "Farmhouse Pizza", quantity: 1, price: 550 }
    ],
    delivery: {
      city: "Mumbai",
      fee: 60
    }
  },
  {
    order_id: 5003,
    restaurant_id: 103,
    customer_name: "Kabir",
    order_date: ISODate("2026-09-03"),
    status: "Delivered",
    items: [
      { name: "Protein Bowl", quantity: 2, price: 400 },
      { name: "Juice", quantity: 1, price: 150 }
    ],
    delivery: {
      city: "Bangalore",
      fee: 50
    }
  },
  {
    order_id: 5004,
    restaurant_id: 101,
    customer_name: "Nisha",
    order_date: ISODate("2026-09-04"),
    status: "Cancelled",
    items: [
      { name: "Veg Biryani", quantity: 1, price: 250 }
    ],
    delivery: {
      city: "Hyderabad",
      fee: 40
    }
  },
  {
    order_id: 5005,
    restaurant_id: 105,
    customer_name: "Rohan",
    order_date: ISODate("2026-09-05"),
    status: "Delivered",
    items: [
      { name: "Thai Curry", quantity: 1, price: 480 },
      { name: "Noodles", quantity: 2, price: 300 }
    ],
    delivery: {
      city: "Delhi",
      fee: 70
    }
  }
])

//  CRUD AND BASIC QUERIES

// Q1
db.restaurants.find()

// Q2
db.restaurants.find({ city: "Hyderabad" })

// Q3
db.restaurants.find({
  active: true,
  rating: { $gt: 4.3 }
})

// Q4
db.restaurants.insertOne({
  restaurant_id: 106,
  restaurant_name: "Taco Town",
  city: "Chennai",
  cuisine: ["Mexican", "Fast Food"],
  rating: 4.0,
  active: true,
  contact: {
    phone: "9444455555",
    email: "taco@email.com"
  }
})

// Q5
db.restaurants.updateOne(
  { restaurant_id: 104 },
  { $set: { rating: 4.1 } }
)

// Q6
db.restaurants.updateOne(
  { restaurant_id: 104 },
  { $set: { active: true } }
)

// Q7
db.restaurants.deleteOne({ restaurant_id: 106 })

//  ARRAYS AND EMBEDDED DOCUMENTS

// Q8
db.restaurants.find({ cuisine: "Fast Food" })

// Q9
db.restaurants.find({ cuisine: { $all: ["Italian", "Fast Food"] } })

// Q10
db.restaurants.updateOne(
  { restaurant_id: 102 },
  { $addToSet: { cuisine: "Desserts" } }
)

// Q11
db.restaurants.updateOne(
  { restaurant_id: 103 },
  { $set: { "contact.email": "greenbowl@email.com" } }
)

// Q12
db.restaurants.find({ "contact.phone": { $regex: /^9/ } })

//  ORDERS

// Q13
db.orders.find({ status: "Delivered" })

// Q14
db.orders.find({ order_date: { $gt: ISODate("2026-09-02") } })

// Q15
db.orders.find({ "delivery.city": "Hyderabad" })

// Q16
db.orders.find({ "items.name": "Noodles" })

// Q17
db.orders.find({ "items.quantity": { $gt: 1 } })

// Q18
db.orders.find({
  items: { $elemMatch: { name: "Chicken Biryani", quantity: 2 } }
})

// Q19
db.orders.updateOne(
  { order_id: 5002 },
  { $push: { items: { name: "Garlic Bread", quantity: 1, price: 180 } } }
)

// Q20
db.orders.updateOne(
  { order_id: 5002 },
  { $set: { status: "Delivered" } }
)

//  PROJECTION AND SORTING

// Q21
db.restaurants.find({}, { restaurant_name: 1, city: 1, rating: 1, _id: 0 })

// Q22
db.restaurants.find().sort({ rating: -1 })

// Q23
db.restaurants.find().sort({ rating: -1 }).limit(3)

//  DATA TYPES

// Q24
db.restaurants.find({ rating: { $type: "number" } })

// Q25
db.orders.aggregate([
  { $project: { _id: 0, order_id: 1, order_date_type: { $type: "$order_date" } } }
])

// Q26
db.orders.aggregate([
  { $project: { _id: 0, order_id: 1, items_type: { $type: "$items" } } }
])

// Q27
db.restaurants.insertOne({
  restaurant_id: 107,
  restaurant_name: "Test Cafe",
  city: "Pune",
  cuisine: ["Cafe", "Snacks"],
  rating: "4.6",
  active: true,
  contact: {
    phone: "9555566666",
    email: "test@email.com"
  }
})

db.restaurants.find({ rating: { $type: "string" } })      // identify

db.restaurants.updateOne(                                  // correct
  { restaurant_id: 107 },
  { $set: { rating: 4.6 } }
)

//DELIVERY PARTNERS

// Q28
db.createCollection("delivery_partners")

db.delivery_partners.insertMany([
  {
    partner_id: 1,
    partner_name: "Ravi Kumar",
    city: "Hyderabad",
    rating: 4.6,
    active: true,
    vehicle: "Bike",
    skills_areas: ["Banjara Hills", "Madhapur", "Hitech City"],
    contact: {
      phone: "9700000001",
      email: "ravi@email.com"
    }
  },
  {
    partner_id: 2,
    partner_name: "Sneha Reddy",
    city: "Hyderabad",
    rating: 3.8,
    active: true,
    vehicle: "Scooter",
    skills_areas: ["Kukatpally", "Miyapur"],
    contact: {
      phone: "9700000002",
      email: "sneha@email.com"
    }
  },
  {
    partner_id: 3,
    partner_name: "Imran Khan",
    city: "Mumbai",
    rating: 4.3,
    active: true,
    vehicle: "Bike",
    skills_areas: ["Andheri", "Bandra"],
    contact: {
      phone: "9700000003",
      email: "imran@email.com"
    }
  },
  {
    partner_id: 4,
    partner_name: "Priya Nair",
    city: "Bangalore",
    rating: 4.8,
    active: false,
    vehicle: "Electric Scooter",
    skills_areas: ["Indiranagar", "Koramangala"],
    contact: {
      phone: "9700000004",
      email: "priya@email.com"
    }
  },
  {
    partner_id: 5,
    partner_name: "Arjun Singh",
    city: "Delhi",
    rating: 4.1,
    active: true,
    vehicle: "Bike",
    skills_areas: ["Connaught Place", "Saket"],
    contact: {
      phone: "9700000005",
      email: "arjun@email.com"
    }
  }
])

// Q29
db.delivery_partners.find({
  active: true,
  city: "Hyderabad"
})

// Q30
db.delivery_partners.find({ rating: { $gt: 4 } })

// Q31
db.delivery_partners.updateOne(
  { partner_id: 1 },
  { $push: { skills_areas: "Gachibowli" } }
)

// Q32
db.delivery_partners.updateOne(
  { partner_id: 2 },
  { $set: { rating: 4.2 } }
)

// Q33
db.delivery_partners.find().sort({ rating: -1 })
