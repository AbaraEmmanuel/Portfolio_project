document.addEventListener('DOMContentLoaded', function() {
    // Function to send AJAX request
    function sendRequest(url, method, data, callback) {
        fetch(url, {
            method: method,
            body: new URLSearchParams(data),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);  // Add this line
            callback(data);
        })
        .catch(error => console.error('Error:', error));
    }

    // Set current date
    document.getElementById('cur-date').addEventListener('click', function() {
        const currentDate = new Date().toISOString().split('T')[0];
        document.getElementById('transaction_date').value = currentDate;
    });

    // Save record
    document.getElementById('submit-btn').addEventListener('click', function() {
        const item_name = document.getElementById('item_name').value;
        const item_amt = document.getElementById('item_amt').value;
        const transaction_date = document.getElementById('transaction_date').value;

        sendRequest('/save_record', 'POST', { 'item_name': item_name, 'item_amt': item_amt, 'transaction_date': transaction_date }, function(data) {
            if (data.status === 'success') {
                document.getElementById('total-expense').textContent = `Total Expense: ${data.total_expense}`;
                document.getElementById('balance-remaining').textContent = `Balance Remaining: ${data.balance_remaining}`;
                document.getElementById('record-form').reset();
                alert(data.message);
            } else {
                alert(data.message);
            }
        });
    });

    // Update record
    document.getElementById('update-btn').addEventListener('click', function() {
        const item_name = document.getElementById('item_name').value;
        const item_amt = document.getElementById('item_amt').value;
        const transaction_date = document.getElementById('transaction_date').value;
        const selected_rowid = document.getElementById('selected_rowid').value;

        sendRequest('/update_record', 'POST', { 'item_name': item_name, 'item_amt': item_amt, 'transaction_date': transaction_date, 'selected_rowid': selected_rowid }, function(data) {
            if (data.status === 'success') {
                document.getElementById('total-expense').textContent = `Total Expense: ${data.total_expense}`;
                document.getElementById('balance-remaining').textContent = `Balance Remaining: ${data.balance_remaining}`;
                document.getElementById('record-form').reset();
                alert(data.message);
            } else {
                alert(data.message);
            }
        });
    });

    // Delete record
    document.getElementById('delete-btn').addEventListener('click', function() {
        const selected_rowid = document.getElementById('selected_rowid').value;

        sendRequest('/delete_record', 'POST', { 'selected_rowid': selected_rowid }, function(data) {
            if (data.status === 'success') {
                document.getElementById('total-expense').textContent = `Total Expense: ${data.total_expense}`;
                document.getElementById('balance-remaining').textContent = `Balance Remaining: ${data.balance_remaining}`;
                alert(data.message);
            } else {
                alert(data.message);
            }
        });
    });

    // Set budget
    document.getElementById('budget-btn').addEventListener('click', function() {
        const budget = prompt("Enter the monthly budget:");

        if (budget !== null && !isNaN(budget)) {
            sendRequest('/set_budget', 'POST', { 'budget': Number(budget) }, function(data) {
                if (data.status === 'success') {
                    document.getElementById('total-expense').textContent = `Total Expense: ${data.total_expense}`;
                    document.getElementById('balance-remaining').textContent = `Balance Remaining: ${data.balance_remaining}`;
                    alert(data.message);
                } else {
                    alert(data.message);
                }
            });
        } else {
            alert("Invalid input! Please enter a valid budget.");
        }
    });

    // Other functionalities can be implemented similarly using AJAX requests
});
