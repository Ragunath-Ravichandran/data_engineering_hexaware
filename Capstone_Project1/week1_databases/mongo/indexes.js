use attendance_tracker

db.task_feedback.createIndex({ employee_id: 1 })
db.task_feedback.createIndex({ department: 1 })
db.task_feedback.createIndex({ employee_id: 1, created_at: -1 })

db.employee_notes.createIndex({ employee_id: 1 })
db.employee_notes.createIndex({ department: 1 })

db.task_feedback.find({ employee_id: 1 })
db.task_feedback.find({ department: "Engineering", rating: { $lte: 3 } })
db.task_feedback.aggregate([
  { $group: { _id: "$department", avg_rating: { $avg: "$rating" } } }
])

db.task_feedback.getIndexes()
