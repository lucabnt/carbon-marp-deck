---
marp: true
footer: "Converter cases"
paginate: true
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Cover
## Subtitle

<!-- Speaker note for the cover: say hello. -->

---

## Code block with a hash and a separator

```bash
# this must NOT become a title
terraform apply
---
echo "still code"
```

<!-- First note line.
Second note line. -->

Text after the code.

---

## Lists

1. First step
2. Second step
   - nested bullet
   - another nested
3. Third step

- plain bullet
  1. nested number
  2. another

---

## Deeply nested lists

- Level 0
  - Level 1
    - Level 2
      - Level 3
  - Level 1 again
    1. Numbered at level 2
    2. Second numbered
- Level 0 again

---

## KPI and diagrams, loose syntax

<div class="cols3">
<div>

<div class="kpi">
  42%
</div>
<div class="kpi-label">
  Multi-line label
</div>

</div>
<div>

![w:200](fixtures/sample.png)

</div>
<div>

```python
# code in a column
print("hi")
```

</div>
</div>

<div class="flow">
  <div class="node"><small>sub first</small><b>Label</b></div>
  <div class="arrow">→</div>
  <div class="node dark">
    <b>Multi
    line</b>
    <small>sub</small>
  </div>
</div>

---

![bg right](fixtures/sample.png)

## Background image and unknown HTML

<video src="x.mp4">

<div class="mystery">

Text inside unknown wrapper.

</div>

---

<!-- _class: section -->
<!-- _paginate: false -->

# Section

<img src="../assets/pictograms/svg/cloud.svg" class="pictogram lg white" alt="">

## Subtitle

---

<!-- _class: end -->
<!-- _paginate: false -->

# Thank you
## Closing slide
