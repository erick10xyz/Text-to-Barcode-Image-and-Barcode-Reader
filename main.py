from __future__ import print_function
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, redirect, url_for, request
import cloudmersive_barcode_api_client
from cloudmersive_barcode_api_client.rest import ApiException

#  Create account to Cloudmersive and use your own Apikey
configuration = cloudmersive_barcode_api_client.Configuration()
configuration.api_key['Apikey'] = 'Your Apikey


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Your own SECRET KEY'
Bootstrap5(app)

# Convert text to barcode and it save as png image file located in main.py path also where you save it
@app.route("/", methods=["GET", "POST"])
def home():
    api_instance = cloudmersive_barcode_api_client.GenerateBarcodeApi(
        cloudmersive_barcode_api_client.ApiClient(configuration))
    if request.method == "POST":
        value = request.form.get("text")
        api_response = api_instance.generate_barcode_qr_code(value)
        with open('qr_code.png', 'wb') as f:
            f.write(eval(api_response))
        redirect (url_for('read_qr'))
    return render_template("index.html")

# Read Barcode image. Paste the path of your barcode image
@app.route("/read", methods=["GET", "POST"])
def read_qr():
    api_instance = cloudmersive_barcode_api_client.BarcodeScanApi(
        cloudmersive_barcode_api_client.ApiClient(configuration))
    if request.method == "POST":
        image_file = request.form.get("path")

        api_response = api_instance.barcode_scan_image(image_file)
        print(api_response)
        return render_template("show.html", content=api_response)
    return render_template("read.html")


if __name__ == "__main__":
    app.run(debug=True)
