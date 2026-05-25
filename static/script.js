document.getElementById("loanForm").addEventListener("submit", async function(e){
e.preventDefault();

let data = {
no_of_dependents: document.getElementById("no_of_dependents").value,
education: document.getElementById("education").value,
self_employed: document.getElementById("self_employed").value,
income_annum: document.getElementById("income_annum").value,
loan_amount: document.getElementById("loan_amount").value,
loan_term: document.getElementById("loan_term").value,
cibil_score: document.getElementById("cibil_score").value,
residential_assets_value: document.getElementById("residential_assets_value").value,
commercial_assets_value: document.getElementById("commercial_assets_value").value,
luxury_assets_value: document.getElementById("luxury_assets_value").value,
bank_asset_value: document.getElementById("bank_asset_value").value
};

let res = await fetch("/predict", {
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify(data)
});

let result = await res.json();

document.getElementById("result").innerHTML = result.result;
});
