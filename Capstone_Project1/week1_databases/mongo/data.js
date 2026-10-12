use attendance_tracker

db.task_feedback.insertMany([
  {
    employee_id: 1,
    department: "Engineering",
    task_title: "Build login module",
    feedback: "Delivered ahead of schedule. Clean code and good documentation.",
    rating: 5,
    reviewer: "Manager A",
    tags: ["quality", "on-time"],
    created_at: new Date("2025-01-10")
  },
  {
    employee_id: 1,
    department: "Engineering",
    task_title: "Fix API bugs",
    feedback: "Needs better root-cause analysis before patching.",
    rating: 3,
    reviewer: "Manager A",
    tags: ["improvement"],
    created_at: new Date("2025-01-13")
  },
  {
    employee_id: 2,
    department: "HR",
    task_title: "Prepare HR report",
    feedback: "Report was accurate and well formatted.",
    rating: 4,
    reviewer: "Director HR",
    tags: ["accuracy"],
    created_at: new Date("2025-01-08")
  },
  {
    employee_id: 3,
    department: "Engineering",
    task_title: "Write test cases",
    feedback: "Good coverage but frequent late logins affect team sync.",
    rating: 3,
    reviewer: "Manager A",
    notes: ["Discussed punctuality", "Follow-up in 2 weeks"],
    tags: ["attendance", "coverage"],
    created_at: new Date("2025-01-11")
  }
])

db.employee_notes.insertMany([
  {
    employee_id: 3,
    department: "Engineering",
    note_type: "attendance",
    note: "Absent on 2025-01-07 without prior intimation.",
    created_by: "HR",
    created_at: new Date("2025-01-08")
  },
  {
    employee_id: 4,
    department: "Finance",
    note_type: "performance",
    note: "Handles reconciliation independently.",
    created_by: "Finance Lead",
    created_at: new Date("2025-01-09")
  }
])
