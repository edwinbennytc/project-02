document.addEventListener('DOMContentLoaded', () => {
    const otpRequestForm = document.getElementById('otpRequestForm');
    const otpVerifyForm = document.getElementById('otpVerifyForm');

    if (otpRequestForm) {
        otpRequestForm.addEventListener('submit', requestOTP);
    }

    if (otpVerifyForm) {
        otpVerifyForm.addEventListener('submit', verifyOTP);
    }
});

async function requestOTP(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;

    try {
        const response = await fetch('https://9uvtrei0hc.execute-api.ap-southeast-2.amazonaws.com/prod/generate-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });

        // Check if the response status is OK
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        // Log the result for debugging
        console.log('API response:', result);
        
        if (result.success) {
            alert('OTP sent successfully!');
        } else {
            alert(`Error requesting OTP: ${result.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error requesting OTP. Please try again.');
    }
}


async function verifyOTP(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const otp = document.getElementById('otp').value;

    try {
        const response = await fetch('https://9uvtrei0hc.execute-api.ap-southeast-2.amazonaws.com/prod/verify-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, otp })
        });

        // Check if the response status is OK
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        // Log the result for debugging
        console.log('API response:', result);
        
        // Display the message from the API response
        if (result.success) {
            alert(result.message);
        } else {
            alert(`Error verifying OTP: ${result.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error verifying OTP. Please try again.');
    }
}
