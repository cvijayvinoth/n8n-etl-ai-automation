# ETL AI Automation in n8n

This architecture guide demonstrates how to build and orchestrate an end-to-end **ETL (Extract, Transform, Load)** pipeline inside n8n.

---

## Pipeline Architecture

```text
[Form Trigger]  -->  [Extract from File]  -->  [Code Node]  -->  [Filter Node]  -->  [Convert to File]
 (Upload CSV)         (Parse Binary)          (Sanitize & Validate) (Filter Criteria)  (Export Clean CSV)
```

---

## Node-by-Node Pipeline Implementation

### 1. Extract Stage: Ingestion & Binary Parsing
- **Node**: `On form submission` (`n8n-nodes-base.formTrigger`, v2.6)
  - Configured with a file upload field: `Upload student data`.
  - Captures binary payload directly into `$binary.Upload_student_data`.
- **Node**: `Extract from File` (`n8n-nodes-base.extractFromFile`, v1.1)
  - Reads `binaryPropertyName: "Upload_student_data"`.
  - Parses CSV into distinct JSON items, setting `headerRow: true`.

### 2. Transform Stage: Data Sanitization & Normalization
- **Node**: `Code in JavaScript` (`n8n-nodes-base.code`, v2)
  - Applies deterministic formatting functions across every item in `$input.all()`.

```javascript
function toTitleCase(str) {
  if (!str) return '';
  return str.toLowerCase().trim().split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function normalizeCourse(course) {
  if (!course) return '';
  const clean = course.trim().toLowerCase();
  if (clean === 'python') return 'Python';
  if (clean === 'ml' || clean === 'machine learning') return 'Machine Learning';
  return toTitleCase(course);
}

return $input.all().map(item => {
  const raw = item.json;
  const name = toTitleCase(raw.Name);
  const email = (raw.Email || '').trim().toLowerCase();
  const city = toTitleCase(raw.City) || 'Not Provided';
  const course = normalizeCourse(raw.Course);
  const feePaid = (raw.Fee_Paid || '').trim().toLowerCase() === 'yes' ? 'Yes' : 'No';
  const rawPhone = (raw.Phone || '').trim();
  const phone = rawPhone.length === 10 ? rawPhone : 'Invalid/Missing';
  const validEmail = isValidEmail(email);

  return {
    json: {
      Student_ID: raw.Student_ID,
      Name: name,
      Email: email,
      Phone: phone,
      Course: course,
      Fee_Paid: feePaid,
      City: city,
      Enrolled_Date: raw.Enrolled_Date,
      is_valid_email: validEmail
    }
  };
});
```

### 3. Filter & Load Stage: Business Logic & Export
- **Node**: `Filter` (`n8n-nodes-base.filter`, v2.3)
  - Combinator: `OR`
  - Condition 1: `is_valid_email == true`
  - Condition 2: `Fee_Paid == 'Yes'`
- **Node**: `Convert to File` (`n8n-nodes-base.convertToFile`, v1.1)
  - Serializes verified JSON stream back into a downloadable binary CSV asset.
