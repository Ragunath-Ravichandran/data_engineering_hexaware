use retail_dashboard

db.campaign_feedback.createIndex({ product: 1 })
db.campaign_feedback.createIndex({ region: 1 })
db.campaign_feedback.createIndex({ product: 1, region: 1 })

db.campaign_feedback.find({ product: "Wireless Mouse" })
db.campaign_feedback.find({ region: "South" })
db.campaign_feedback.find({ avg_rating: { $lt: 3 } })

db.campaign_feedback.aggregate([
  { $group: { _id: "$region", avg_rating: { $avg: "$avg_rating" }, campaigns: { $sum: 1 } } }
])

db.campaign_feedback.getIndexes()
