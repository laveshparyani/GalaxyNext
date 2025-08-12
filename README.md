# GalaxyNext

[![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Frappe](https://img.shields.io/badge/framework-Frappe-green.svg)](https://frappeframework.com/)

## Overview

GalaxyNext is a comprehensive Enterprise Resource Planning (ERP) system built on the robust Frappe Framework with ERPNext as its core. It features custom modules, India GST compliance, OpenAI integration, and comprehensive business management tools designed for modern enterprises.

## 🚀 Features

### Core ERP Functionality
- **Financial Management**: Complete accounting, banking, and financial reporting
- **Inventory Management**: Stock tracking, warehouse management, and procurement
- **Sales & CRM**: Customer relationship management and sales pipeline
- **Manufacturing**: Production planning, work orders, and quality control
- **Human Resources**: Employee management, payroll, and attendance
- **Project Management**: Task tracking, time logging, and project analytics

### Custom Modules
- Enhanced business intelligence and reporting
- Advanced workflow automation
- Custom business logic and extensions
- Tailored user experience and dashboards

### India Compliance Features
- **GST India**: Complete GST compliance and reporting
- **Income Tax India**: Tax calculation and filing support
- **Audit Trail**: Comprehensive compliance tracking
- Regional business rule support

### AI Integration
- **OpenAI Integration**: AI-powered business insights
- Smart document processing
- Intelligent data analysis
- Automated decision support

## 🛠️ Technology Stack

- **Backend**: Python 3.12, Frappe Framework
- **Database**: MariaDB/MySQL
- **Frontend**: Frappe Desk, JavaScript, HTML5, CSS3
- **Cache**: Redis
- **Web Server**: Nginx/Apache
- **AI**: OpenAI API Integration

## 📋 Prerequisites

- Python 3.12+
- Node.js 18+
- Redis
- MariaDB/MySQL 10.3+
- Git

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/GalaxyNext.git
cd GalaxyNext
```

### 2. Set Up Frappe Bench
```bash
# Install Frappe Bench
curl -sL https://git.io/frappe-bench | bash -s develop

# Navigate to bench directory
cd frappe-bench
```

### 3. Create New Site
```bash
bench new-site galaxynext.com
bench --site galaxynext.com add-to-hosts
```

### 4. Install Apps
```bash
bench --site galaxynext.com install-app erpnext
bench --site galaxynext.com install-app galaxyerp
bench --site galaxynext.com install-app india_compliance
bench --site galaxynext.com install-app frappe_openai_integration
```

### 5. Set Up Environment
```bash
# Activate virtual environment
source env/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 6. Configure Environment Variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
FRAPPE_SITE_URL=http://galaxynext.com
```

### 7. Start the Application
```bash
bench start
```

## 🌐 Access

- **Frontend**: http://galaxynext.com
- **Admin Panel**: http://galaxynext.com/app
- **API Documentation**: http://galaxynext.com/api/method/frappe.utils.print_format.download_pdf

## 📚 Documentation

- [Frappe Framework Documentation](https://frappeframework.com/docs)
- [ERPNext User Manual](https://docs.erpnext.com/)
- [India Compliance Documentation](https://docs.india-compliance.org/)

## 🔧 Configuration

### OpenAI Integration
1. Obtain API key from [OpenAI](https://platform.openai.com/)
2. Add to environment variables
3. Configure in Frappe Desk > Setup > Integrations > OpenAI

### India Compliance
1. Configure GST settings in ERPNext
2. Set up company details with GST numbers
3. Enable required compliance features

## 🧪 Testing

```bash
# Run tests
bench --site galaxynext.com run-tests

# Run specific app tests
bench --site galaxynext.com run-tests --app galaxyerp
```

## 📦 Deployment

### Production Setup
```bash
# Build assets
bench build

# Setup production
bench setup production

# Start production server
bench start --production
```

### Docker Deployment
```bash
# Build Docker image
docker build -t galaxynext .

# Run container
docker run -p 8000:8000 galaxynext
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)** - see the [LICENSE](LICENSE) file for details.

### What GPL-3.0 Means for You:

**You Can:**
- Use the software for any purpose
- Study how the software works
- Modify the software
- Distribute the original or modified software
- Share the software with others

**You Cannot:**
- **Make it proprietary** - You can't take our code, change it, and then close the source. You must also release your modified version under GPLv3.
- **Remove our copyright/license** - You must preserve our copyright and the GPL license notice in your modified version.
- **Distribute without source code** - If you distribute the software (even if modified), you must make the full source code available.
- **Restrict others from copying/sharing** - Any users of your version must also have the same rights to use, study, modify, and share it.

**In simple terms:** If you use, modify, or distribute this software, you must keep it open source and give others the same freedoms you received.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/GalaxyNext/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/GalaxyNext/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/GalaxyNext/wiki)

## 🙏 Acknowledgments

- [Frappe Framework](https://frappeframework.com/) - The amazing web framework
- [ERPNext](https://erpnext.com/) - The world's best open-source ERP
- [India Compliance](https://india-compliance.org/) - India-specific compliance features
- All contributors and community members

## 📊 Project Status

- **Version**: 1.0.0
- **Status**: Active Development
- **Last Updated**: January 2025

---

**Made with ❤️ by the GalaxyNext Team**

For more information, visit [galaxynext.com](http://galaxynext.galaxyerpsoftware.com:8000/)
