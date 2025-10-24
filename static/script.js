const backendURL =
  window.location.hostname === "localhost"
    ? "http://localhost:10000"
    : window.location.origin;

// Submit Employee Form
document.getElementById("employeeForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = {
    name: document.getElementById("name").value,
    designation: document.getElementById("designation").value,
    salary: document.getElementById("salary").value,
    gender: document.getElementById("gender").value,
    address: document.getElementById("address").value,
    company: document.getElementById("company").value
  };
  try {
    const res = await fetch(`${backendURL}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    const result = await res.json();
    document.getElementById("response").innerText = result.message;
    document.getElementById("employeeForm").reset();
  } catch (err) {
    console.error(err);
    document.getElementById("response").innerText = "Error saving data!";
  }
});

// Search Employees
document.getElementById("searchBtn")?.addEventListener("click", async () => {
  const field = document.getElementById("searchField").value;
  const value = document.getElementById("searchValue").value.trim();
  if (!value) return alert("Please enter a search value");

  try {
    const res = await fetch(`${backendURL}/search?field=${field}&value=${value}`);
    const data = await res.json();
    displayResults(data);
  } catch (err) {
    console.error(err);
    alert("Error searching data!");
  }
});

// Show All Employees
document.getElementById("showAllBtn")?.addEventListener("click", async () => {
  try {
    const res = await fetch(`${backendURL}/all`);
    const data = await res.json();
    displayResults(data);
  } catch (err) {
    console.error(err);
    alert("Error fetching data!");
  }
});

// Display Results
function displayResults(data) {
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";
  if (!data.results || data.results.length === 0) {
    resultsDiv.innerHTML = `<p style="text-align:center;color:red;">No records found!</p>`;
    return;
  }
  let table = `<table>
      <tr>
          <th>ID</th><th>Name</th><th>Designation</th><th>Salary</th>
          <th>Gender</th><th>Address</th><th>Company</th>
      </tr>`;
  data.results.forEach(r => {
    table += `<tr>
        <td>${r.id}</td><td>${r.name}</td><td>${r.designation}</td>
        <td>${r.salary}</td><td>${r.gender}</td><td>${r.address}</td>
        <td>${r.company}</td>
    </tr>`;
  });
  table += `</table>`;
  resultsDiv.innerHTML = table;
}
