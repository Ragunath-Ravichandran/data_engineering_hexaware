//use commerce_assessment

db.createCollection("products")

db.products.insertMany([
  {
    product_id: 101,
    product_name: "Ultra Laptop",
    category: "Electronics",
    brand: "TechPro",
    price: 72000,
    stock: 12,
    available: true,
    launch_date: ISODate("2026-01-15"),
    colors: ["Black", "Silver"],
    specifications: {
      ram: "16 GB",
      storage: "1 TB SSD",
      warranty_years: 2
    }
  },
  {
    product_id: 102,
    product_name: "Wireless Mouse",
    category: "Accessories",
    brand: "ClickMax",
    price: 1800,
    stock: 40,
    available: true,
    launch_date: ISODate("2026-02-10"),
    colors: ["Black", "Blue", "Red"],
    specifications: {
      wireless: true,
      warranty_years: 1
    }
  },
  {
    product_id: 103,
    product_name: "Office Desk",
    category: "Furniture",
    brand: "WorkSpace",
    price: 14500,
    stock: 8,
    available: true,
    launch_date: ISODate("2025-11-20"),
    colors: ["Brown", "Black"],
    specifications: {
      material: "Wood",
      adjustable: false,
      warranty_years: 3
    }
  },
  {
    product_id: 104,
    product_name: "Smart Monitor",
    category: "Electronics",
    brand: "VisionPlus",
    price: 26000,
    stock: 5,
    available: true,
    launch_date: ISODate("2026-03-01"),
    colors: ["Black"],
    specifications: {
      screen_size: "27 inch",
      resolution: "4K",
      warranty_years: 2
    }
  },
  {
    product_id: 105,
    product_name: "Gaming Chair",
    category: "Furniture",
    brand: "SeatPro",
    price: 18500,
    stock: 0,
    available: false,
    launch_date: ISODate("2026-01-05"),
    colors: ["Black", "Red"],
    specifications: {
      material: "Leather",
      adjustable: true,
      warranty_years: 3
    }
  },
  {
    product_id: 106,
    product_name: "Mechanical Keyboard",
    category: "Accessories",
    brand: "KeyWorks",
    price: 5200,
    stock: 18,
    available: true,
    launch_date: ISODate("2026-04-12"),
    colors: ["Black", "White"],
    specifications: {
      backlit: true,
      wireless: false,
      warranty_years: 1
    }
  }
])

//PART 2 - CRUD OPERATIONS

// Q1
db.products.find()

// Q2
db.products.findOne({ product_id: 103 })

// Q3
db.products.insertOne({
  product_id: 107,
  product_name: "Bluetooth Speaker",
  category: "Electronics",
  brand: "SoundMax",
  price: 7500,
  stock: 20,
  available: true
})

// Q4
db.products.insertMany([
  {
    product_id: 108,
    product_name: "USB Hub",
    category: "Accessories",
    brand: "PortMax",
    price: 1200,
    stock: 30,
    available: true
  },
  {
    product_id: 109,
    product_name: "Webcam HD",
    category: "Electronics",
    brand: "ViewCam",
    price: 3500,
    stock: 0,
    available: false
  }
])

// Q5
db.products.updateOne(
  { product_id: 102 },
  { $set: { price: 2000 } }
)

// Q6
db.products.updateOne(
  { product_id: 105 },
  { $set: { stock: 15, available: true } }
)

// Q7
db.products.updateOne(
  { product_id: 104 },
  { $inc: { stock: 10 } }
)

// Q8
db.products.updateOne(
  { product_id: 106 },
  { $inc: { stock: -3 } }
)

// Q9
db.products.updateOne(
  { product_id: 101 },
  { $set: { discount_percent: 10 } }
)

// Q10
db.products.updateOne(
  { product_id: 101 },
  { $unset: { discount_percent: "" } }
)

// Q11
db.products.find({ product_id: 108 })          // before delete
db.products.deleteOne({ product_id: 108 })
db.products.find({ product_id: 108 })          // after delete

// Q12
db.products.find({ stock: 0 })                 // before delete
db.products.deleteMany({ stock: 0 })
db.products.find({ stock: 0 })                 // after delete

// Q13
// Verification done above 
// PART 3 - FILTERING AND QUERY OPERATORS


// Q14
db.products.find({ category: "Electronics" })

// Q15
db.products.find({ price: { $gt: 10000 } })

// Q16
db.products.find({ price: { $gte: 5000, $lte: 30000 } })

// Q17
db.products.find({ stock: { $lt: 10 } })

// Q18
db.products.find({ available: true })

// Q19
db.products.find({ available: false })

// Q20
db.products.find({ category: { $in: ["Electronics", "Furniture"] } })

// Q21
db.products.find({ category: { $ne: "Accessories" } })

// Q22
db.products.find({
  price: { $gt: 10000 },
  stock: { $gt: 5 }
})

// Q23
db.products.find({
  $or: [
    { category: "Electronics" },
    { price: { $lt: 5000 } }
  ]
})

// Q24
db.products.find({ launch_date: { $gt: ISODate("2026-02-01") } })

// Q25
db.products.find({
  launch_date: {
    $gte: ISODate("2026-01-01"),
    $lte: ISODate("2026-03-31")
  }
})

// PART 4 - PROJECTION AND SORTING

// Q26
db.products.find({}, { product_name: 1, price: 1, _id: 0 })

// Q27
db.products.find({}, { product_name: 1, category: 1, stock: 1 })

// Q28
db.products.find().sort({ price: 1 })

// Q29
db.products.find().sort({ price: -1 })

// Q30
db.products.find().sort({ product_name: 1 })

// Q31
db.products.find().sort({ price: -1 }).limit(3)

// Q32
db.products.find().sort({ stock: 1 }).limit(2)



//  PART 5 - ARRAYS


// Q33
db.products.find({ colors: "Black" })

// Q34
db.products.find({ colors: { $all: ["Black", "Silver"] } })

// Q35
db.products.find({ colors: { $in: ["White", "Blue"] } })

// Q36
db.products.updateOne(
  { product_id: 101 },
  { $push: { colors: "Grey" } }
)

// Q37
db.products.updateOne(
  { product_id: 101 },
  { $addToSet: { colors: "Black" } }
)

// Q38
db.products.updateOne(
  { product_id: 102 },
  { $pull: { colors: "Red" } }
)

// Q39
db.products.find({ "colors.1": { $exists: true } })



//  PART 6 - EMBEDDED DOCUMENTS


// Q40
db.products.find({ "specifications.warranty_years": 2 })

// Q41
db.products.find({ "specifications.adjustable": true })

// Q42
db.products.find({ "specifications.wireless": true })

// Q43
db.products.updateOne(
  { product_id: 103 },
  { $set: { "specifications.warranty_years": 5 } }
)

// Q44
db.products.updateMany(
  { product_id: { $in: [101, 104] } },
  { $set: { "specifications.country_of_origin": "India" } }
)

// Q45
db.products.find({ "specifications.country_of_origin": "India" })



//  PART 7 - DATA TYPES


// Q46
db.products.find({ price: { $type: "number" } })

// Q47
db.products.aggregate([
  { $project: { _id: 0, product_id: 1, launch_date_type: { $type: "$launch_date" } } }
])

// Q48
db.products.aggregate([
  { $project: { _id: 0, product_id: 1, colors_type: { $type: "$colors" } } }
])

// Q49
db.products.aggregate([
  { $project: { _id: 0, product_id: 1, specifications_type: { $type: "$specifications" } } }
])

// Q50
db.products.insertOne({
  product_id: 110,
  product_name: "Portable SSD",
  category: "Electronics",
  brand: "DataFast",
  price: "25000",
  stock: 14,
  available: true
})

// Q51
db.products.find({ price: { $type: "string" } })

// Q52
db.products.updateOne(
  { product_id: 110 },
  { $set: { price: 25000 } }
)



//  PART 8 - CUSTOMERS COLLECTION


db.createCollection("customers")

db.customers.insertMany([
  {
    customer_id: 501,
    customer_name: "Aditya Rao",
    email: "aditya@email.com",
    active: true,
    address: {
      city: "Hyderabad",
      state: "Telangana",
      pincode: "500081"
    },
    interests: ["Electronics", "Accessories"]
  },
  {
    customer_id: 502,
    customer_name: "Maya Thomas",
    email: "maya@email.com",
    active: true,
    address: {
      city: "Chennai",
      state: "Tamil Nadu",
      pincode: "600028"
    },
    interests: ["Furniture", "Home"]
  },
  {
    customer_id: 503,
    customer_name: "Faisal Ahmed",
    email: "faisal@email.com",
    active: false,
    address: {
      city: "Hyderabad",
      state: "Telangana",
      pincode: "500034"
    },
    interests: ["Electronics"]
  },
  {
    customer_id: 504,
    customer_name: "Nikita Shah",
    email: "nikita@email.com",
    active: true,
    address: {
      city: "Mumbai",
      state: "Maharashtra",
      pincode: "400050"
    },
    interests: ["Furniture", "Electronics"]
  }
])

// Q53
db.customers.find()

// Q54
db.customers.find({ active: true })

// Q55
db.customers.find({ "address.city": "Hyderabad" })

// Q56
db.customers.find({ interests: "Electronics" })

// Q57
db.customers.find({ interests: { $all: ["Furniture", "Electronics"] } })

// Q58
db.customers.updateOne(
  { customer_id: 503 },
  { $set: { active: true } }
)

// Q59
db.customers.updateOne(
  { customer_id: 504 },
  { $set: { "address.city": "Pune" } }
)

// Q60
db.customers.updateOne(
  { customer_id: 502 },
  { $addToSet: { interests: "Decor" } }
)



//  PART 9 - ARRAY OF EMBEDDED DOCUMENTS (ORDERS)


db.createCollection("orders")

db.orders.insertMany([
  {
    order_id: 9001,
    customer_id: 501,
    order_date: ISODate("2026-09-01"),
    status: "Delivered",
    items: [
      { product: "Ultra Laptop", quantity: 1, price: 72000 },
      { product: "Wireless Mouse", quantity: 2, price: 2000 }
    ]
  },
  {
    order_id: 9002,
    customer_id: 502,
    order_date: ISODate("2026-09-03"),
    status: "Processing",
    items: [
      { product: "Office Desk", quantity: 1, price: 14500 }
    ]
  },
  {
    order_id: 9003,
    customer_id: 503,
    order_date: ISODate("2026-09-05"),
    status: "Delivered",
    items: [
      { product: "Smart Monitor", quantity: 2, price: 26000 },
      { product: "Mechanical Keyboard", quantity: 1, price: 5200 }
    ]
  }
])

// Q61
db.orders.find({ status: "Delivered" })

// Q62
db.orders.find({ "items.product": "Ultra Laptop" })

// Q63
db.orders.find({ "items.quantity": { $gt: 1 } })

// Q64
db.orders.find({
  items: { $elemMatch: { product: "Smart Monitor", quantity: 2 } }
})

// Q65
db.orders.updateOne(
  { order_id: 9002 },
  { $push: { items: { product: "Gaming Chair", quantity: 1, price: 18500 } } }
)

// Q66
db.orders.updateOne(
  { order_id: 9002 },
  { $set: { status: "Delivered" } }
)

// Q67
db.orders.updateOne(
  { order_id: 9001 },
  { $pull: { items: { product: "Wireless Mouse" } } }
)



//  PART 10 - DOCUMENT DESIGN (ANSWERS)


// Q68: Array
//      A small list of simple values.
//
// Q69: Embedded Document
//      One-to-one data, always read together with the customer.
//
// Q70: Array of Embedded Documents
//      Each line item has its own fields (product, quantity, price).
//
// Q71: Embedded Document
//      A fixed group of related attributes of one product.
//
// Q72: Separate Collection / Reference
//      Orders grow without limit, so they should not live inside the customer.
//
// Q73: Separate Collection / Reference
//      Millions of reviews would bloat the product document.
//
// Q74: Simple Field
//      first_name and last_name are plain values.
//
// Q75: Array
//      A list of simple strings.



//SUPPLIERS


db.createCollection("suppliers")

db.suppliers.insertMany([
  {
    supplier_id: 1,
    supplier_name: "TechSource India",
    city: "Hyderabad",
    active: true,
    categories: ["Electronics", "Accessories"],
    contact: {
      phone: "9876500001",
      email: "sales@techsource.com"
    },
    warehouses: ["Hyderabad-HiTec", "Bangalore-Whitefield"],
    registration_date: ISODate("2025-06-10")
  },
  {
    supplier_id: 2,
    supplier_name: "HomeNest Furnishings",
    city: "Chennai",
    active: true,
    categories: ["Furniture", "Home"],
    contact: {
      phone: "9876500002",
      email: "contact@homenest.com"
    },
    warehouses: ["Chennai-Guindy", "Coimbatore-Peelamedu"],
    registration_date: ISODate("2026-02-18")
  },
  {
    supplier_id: 3,
    supplier_name: "Gadget Hub",
    city: "Mumbai",
    active: false,
    categories: ["Electronics", "Gadgets"],
    contact: {
      phone: "9876500003",
      email: "info@gadgethub.com"
    },
    warehouses: ["Mumbai-Andheri", "Pune-Hinjewadi"],
    registration_date: ISODate("2026-03-05")
  },
  {
    supplier_id: 4,
    supplier_name: "OfficeWorks",
    city: "Hyderabad",
    active: true,
    categories: ["Furniture", "Stationery"],
    contact: {
      phone: "9876500004",
      email: "hello@officeworks.com"
    },
    warehouses: ["Hyderabad-Uppal", "Vizag-Gajuwaka"],
    registration_date: ISODate("2025-12-01")
  },
  {
    supplier_id: 5,
    supplier_name: "KeyPoint Peripherals",
    city: "Delhi",
    active: true,
    categories: ["Accessories", "Electronics"],
    contact: {
      phone: "9876500005",
      email: "support@keypoint.com"
    },
    warehouses: ["Delhi-Okhla", "Noida-Sector62"],
    registration_date: ISODate("2026-05-20")
  }
])

// Q76
db.suppliers.find({ active: true })

// Q77
db.suppliers.find({ city: "Hyderabad" })

// Q78
db.suppliers.find({ categories: "Electronics" })

// Q79
db.suppliers.find({ registration_date: { $gt: ISODate("2026-01-01") } })

// Q80
db.suppliers.updateOne(
  { supplier_id: 1 },
  { $push: { warehouses: "Chennai-Ambattur" } }
)

// Q81
db.suppliers.updateOne(
  { supplier_id: 3 },
  { $set: { active: true } }
)

// Q82
db.suppliers.updateOne(
  { supplier_id: 4 },
  { $pull: { categories: "Stationery" } }
)

// Q83
db.suppliers.find({}, { supplier_name: 1, city: 1, _id: 0 })

// Q84
db.suppliers.find().sort({ registration_date: 1 })

// Q85
// Array for categories:
//   A supplier supplies several categories, each a simple string,
//   and { categories: "Electronics" } queries them easily.
//
// Embedded document for contact:
//   Phone and email form one fixed group that belongs to exactly
//   one supplier and is always read together with it.
//
// Array for warehouse locations:
//   A supplier has a small, bounded list of warehouses, and
//   $push / $pull make adding or removing one simple.
