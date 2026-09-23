document.getElementById('kassForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent page reload
    
    const formData = {
        name: document.getElementById('empName').value,
        kgid: document.getElementById('kgidNumber').value,
        aadhaar: document.getElementById('aadhaar').value
    };

    console.log("KASS Form Data Captured:", formData);
    alert("Form submitted successfully! Check console for data.");
});
