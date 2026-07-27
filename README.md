# Azure Custom Vision — Image Classifier

A Python (Flask) web app that classifies an uploaded image using your Azure Custom Vision model.  
Paste your **Prediction URL** and **Prediction Key** on the web page, choose an image, and view the results.

This guide follows the workflow in **Custom Vision.pdf** (class materials). Replace placeholders such as `SXX` with your own student number / assigned values.

---

## Prerequisites

- Python 3.10+
- An Azure account (class subscription)
- A computer with a web browser

---

## Part A — Create Custom Vision resources in Azure

### 1. Open the Azure Portal and sign in

1. Go to: https://azure.microsoft.com/en-us/get-started/azure-portal  
2. Click **Sign in**.  
3. Sign in with your class account (for example: `ERB-Class00-sXX@....onmicrosoft.com`).

### 2. Open Custom Vision

1. On the Azure home page, click **More services**.  
2. Under **AI + machine learning**, click **Custom vision**.  
3. Click **+ Create**.

### 3. Configure the resource

On the **Create Custom Vision** page (**Basics** tab):

1. **Create options:** select **Both** (Training + Prediction).  
2. **Subscription:** keep your class subscription.  
3. **Resource group:** enter / select your group, for example:  
   `RGP_0000001_SXX`  
4. **Region:** for example **(US) East US**.  
5. **Name (instance name):** for example:  
   `SXX-Res`  
6. **Training pricing tier:** **Standard S0**.  
7. **Prediction pricing tier:** **Standard S0**.  
8. Click **Review + create**, then **Create**.

### 4. Wait for deployment

1. Wait until the status shows **Your deployment is complete**.  
2. You should see both:
   - a **Training** resource (for example `SXX-Res`)
   - a **Prediction** resource (for example `SXX-Res-Prediction`)
3. Click **Go to resource group** (or open **Custom vision** again) and confirm both resources show **Succeeded**.

### 5. Open the Custom Vision portal from Azure

1. Open your **Training** resource (for example `SXX-Res`).  
2. In **Get started**, click **Custom Vision portal**.  
   Or go directly to: https://www.customvision.ai/

---

## Part B — Create and train a project

### 6. Sign in to Custom Vision and create a project

1. Open https://www.customvision.ai/ and click **SIGN IN** (use the same Azure account).  
2. Accept the **Terms of Service** (check the box → **I agree**).  
3. Click **NEW PROJECT**.  
4. Fill in:
   - **Name:** for example `Finger heart` (or your own project name)
   - **Resource:** select your training resource (for example `SXX-Res [S0]`)
   - **Project Types:** **Classification**
   - **Classification Types:** **Multiclass (Single tag per image)**
   - **Domains:** **General [A2]** (or another suitable domain)
5. Click **Create project**.

### 7. Prepare a dataset

1. Download images from a dataset site such as: https://www.kaggle.com/  
2. Collect:
   - **Positive images** (the class you want to detect), and  
   - **Negative / other images** (examples that are *not* that class)  
3. Supported upload formats in Custom Vision: **JPG, PNG, BMP** (up to about **6 MB** per image for training).

### 8. Upload and tag positive images

1. In your project, open the **Training Images** tab.  
2. Click **Add images**.  
3. Select your positive images and click **Open**.  
4. In the upload dialog, add a tag (for example `finger_heart`).  
5. Click **Upload … files**, then **Done**.

### 9. Create a negative tag and upload other images

1. In the left **Tags** panel, click **+**.  
2. Create a tag such as `Not finger_heart`.  
3. Check **Is Negative?** if you want it treated as a negative tag, then **Save**.  
4. Click **Add images** again.  
5. Select images that are **not** the target class.  
6. Tag them as `Not finger_heart` (or your negative tag).  
7. Click **Upload … files**, then **Done**.

You should now see image counts under each tag (for example 23 for the positive tag and 18 for the negative tag).

### 10. Train the model

1. Click the green **Train** button.  
2. Choose **Quick Training**.  
3. Click **Train**.  
4. Wait until training finishes on the **Performance** tab (for example **Iteration 1**).

### 11. Quick-test the model (optional but recommended)

1. On the **Performance** tab, click **Quick Test**.  
2. Click **Browse local files** and open a test image.  
3. Confirm the predictions look reasonable (tag name + probability).

### 12. Publish the iteration

1. Stay on the **Performance** tab and select your trained iteration (for example **Iteration 1**).  
2. Click **Publish**.  
3. In **Publish Model**:
   - **Model name:** for example `Iteration1`
   - **Prediction resource:** select your prediction resource (for example `SXX-Res-Prediction`)
4. Click **Publish**.  
5. Confirm the iteration shows as **Published**.

### 13. Copy the Prediction URL and Prediction Key

1. On the **Performance** tab, click **Prediction URL**.  
2. In **How to use the Prediction API**, use the section **If you have an image file**.  
3. Copy:
   - the full **Prediction Endpoint (URL)** ending in `/image`  
   - the **Prediction-Key**

Example format (fake values only):

```text
Prediction URL:
https://your-resource-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/00000000-0000-0000-0000-000000000000/classify/iterations/Iteration1/image

Prediction Key:
your-prediction-key-here
```

The URL already contains:

| Part | Meaning |
|------|---------|
| `https://....cognitiveservices.azure.com` | Endpoint |
| GUID after `/Prediction/` | Project ID |
| Name after `/iterations/` | Published iteration name |

---

## Part C — Run this web app

### 14. Install and start the server

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

Or:

- **Mac:** double-click `start-server.command`  
- **Windows:** double-click `start-server.bat`  

Close that window (or press Ctrl+C) to stop the server.

Open: http://127.0.0.1:8080

### 15. Classify an image

1. Paste your **Prediction URL** into the form.  
2. Paste your **Prediction Key**.  
3. Choose an image.  
4. Click **Classify Image**.  
5. Results appear below the image (top label + confidence bars).

---

## Security note

Do not share your real Prediction Key or commit it to GitHub.  
This app is intended for local / class demo use. Do not expose it publicly without access control.

---

## Troubleshooting

| Problem | What to check |
|---------|----------------|
| Invalid Prediction URL | URL must be a Custom Vision classify URL ending in `/image` or `/url` |
| Invalid Prediction Key | Copy the key again from **Prediction URL** dialog or Azure **Keys and Endpoint** |
| 404 / check project or iteration | Model must be **published**; use the published model name (for example `Iteration1`) |
| Poor accuracy | Add more varied training images, retrain, and publish a new iteration |
