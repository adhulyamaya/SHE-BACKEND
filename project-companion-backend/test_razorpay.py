import razorpay

client = razorpay.Client(auth=("rzp_test_koUzHjjQS5ZfrA", "osRfLNqVm8hUu7nSQmvRSYxH"))

try:
    order = client.order.create({"amount": 500, "currency": "INR", "payment_capture": "0"})
    print(order)
except Exception as e:
    print(f"Error: {str(e)}")
