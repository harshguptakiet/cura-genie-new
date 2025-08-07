# 📸 Profile Photo Setup Guide

## How to Add Your Profile Photo

Your landing page is currently showing a placeholder for your profile picture. Follow these simple steps to add your actual photo:

### Option 1: Replace the Placeholder File ✅ **RECOMMENDED**

1. **Prepare your photo:**
   - Use a **square format** (400x400px or higher recommended)
   - Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`
   - Choose a professional photo with good lighting

2. **Replace the file:**
   - Navigate to the `assets/` folder in your project
   - Delete the current `harsh-gupta-profile.jpg` file
   - Add your photo with the **exact same name**: `harsh-gupta-profile.jpg`

3. **Refresh your browser** - Your photo will appear with perfect circular styling!

### Option 2: Use a Different Filename

If you want to keep your photo with a different name:

1. **Add your photo** to the `assets/` folder with any name (e.g., `my-photo.jpg`)

2. **Update the HTML:**
   - Open `index.html`
   - Find line 333: `src="assets/harsh-gupta-profile.jpg"`
   - Change it to: `src="assets/your-photo-name.jpg"`

3. **Save and refresh** your browser

## 🎨 Current Placeholder

Right now, you'll see a blue placeholder with your initials "HG" until you add your actual photo. This ensures the layout looks professional even without the photo.

## ✨ Automatic Features

Once you add your photo, you'll automatically get:
- **Perfect circular crop**
- **Hover effects and animations**
- **Professional glow effects**
- **Responsive sizing on all devices**
- **Loading fallback if image fails**

## 🔄 Testing Your Setup

1. Start your local server: `python -m http.server 8080`
2. Open: `http://localhost:8080`
3. Scroll to the "Meet the Developer" section
4. Your photo should appear in a beautiful circular frame!

---

**Need help?** Your current contact info is already perfectly integrated:
- 📧 guptasecularharsh@gmail.com
- 📱 +91 8081434149
- 💼 linkedin.com/in/harsh-gupta-kiet/
