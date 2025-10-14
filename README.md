# Crowdfunding Template Processing Automation System

A comprehensive Python automation system for processing crowdfunding campaign templates with brand-specific context injection, validation, and state management.

## 🎯 Overview

This system systematically processes crowdfunding campaign templates in the correct order, injecting brand-specific context while maintaining guardrails to prevent hallucination of critical brand details. It's designed for IDE integration and supports both single-template and bulk processing modes.

## 🚀 Features

- **Brand Context Injection**: Automatically injects brand-specific details into template placeholders
- **Validation System**: Prevents hallucination with comprehensive brand requirement validation
- **State Management**: Tracks processing progress and enables resume functionality
- **CLI Interface**: Supports both single-template and bulk processing modes
- **IDE Compatible**: Designed for seamless integration with development environments
- **Future-Ready**: Framework prepared for OpenRouter API integration (Phase 2)

## 📁 Project Structure

```
wiki/
├── crowdfunding_automation.py    # Main automation script
├── brand_requirements.yaml       # Brand configuration and validation rules
├── PRD.md                       # Product Requirements Document
├── requirements.txt             # Python dependencies
├── README.md                    # This documentation
├── prompt-templates/            # Template files directory
│   ├── summary.md              # Processing order and workflow
│   ├── buyerpersona.md         # Buyer persona template
│   ├── competitor-summary.md   # Competitor analysis template
│   ├── mds.md                  # Market description template
│   ├── voice-and-tone.md       # Brand voice template
│   ├── landingpage-copy.md     # Landing page copy template
│   ├── precampaign-ads-copy.md # Pre-campaign ads template
│   └── campaign-page-copy.md   # Campaign page template
├── output/                     # Generated output directory
│   └── [brand-name]/          # Brand-specific output folder
└── state/                     # Processing state files
    └── [brand-name]_state.json
```

## 🛠 Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd "/Users/sheshnarayaniyer/2025/Zack ai/wiki"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify brand configuration**:
   ```bash
   python crowdfunding_automation.py --validate-brand zack-ai
   ```

## 📋 Usage

### Command Line Interface

#### Single Template Processing
```bash
# Process a specific template
python crowdfunding_automation.py --template buyerpersona --brand zack-ai

# Process with verbose logging
python crowdfunding_automation.py --template mds --brand zack-ai --verbose
```

#### Bulk Processing
```bash
# Process all templates in order
python crowdfunding_automation.py --bulk --brand zack-ai

# Start from a specific template
python crowdfunding_automation.py --bulk --brand zack-ai --start-from voice-and-tone
```

#### Resume Processing
```bash
# Resume from last checkpoint
python crowdfunding_automation.py --resume --brand zack-ai
```

#### Validation
```bash
# Validate brand configuration
python crowdfunding_automation.py --validate-brand zack-ai
```

### Template Processing Order

Based on `prompt-templates/summary.md`, templates are processed in this order:

1. **buyerpersona** - Define target audience
2. **competitor-summary** - Analyze competition
3. **product-description** - Detail product features
4. **Product-positioning-summary** - Position against competitors
5. **mds** - Market description and strategy
6. **voice-and-tone** - Establish brand voice
7. **landingpage-copy** - Create landing page content
8. **precampaign-ads-copy** - Pre-launch advertising
9. **welcome-email-sequence** - Onboarding emails
10. **prelaunch-email-campaign-sequence** - Pre-launch emails
11. **launch-campaign-email-sequence** - Launch emails
12. **campaign-page-copy** - Main campaign page
13. **campaign-videoscript** - Video content script
14. **livecampaigns-ads-copy** - Live campaign ads
15. **pressrelease-copy** - Press release content

## 🔧 Configuration

### Brand Requirements (`brand_requirements.yaml`)

The system uses a comprehensive YAML configuration file that defines:

- **Brand Identity**: Name, product name, tagline
- **Product Specifications**: Pricing tiers, features, technical specs
- **Target Market**: Primary audience, demographics
- **Value Propositions**: Key benefits and differentiators
- **Validation Rules**: Prohibited claims, required disclaimers
- **Campaign Specifics**: Funding goals, timeline, delivery

### Template Placeholders

Common placeholders automatically replaced:
- `[PRODUCT]` / `[PRODUCT NAME]` → Product name
- `[BRAND]` / `[BRAND NAME]` → Brand name
- `[PRICE]` → Standard pricing
- `[EARLY BIRD PRICE]` → Early bird pricing
- `[TARGET AUDIENCE]` → Primary audience
- `[VALUE PROPOSITION]` → Primary value proposition
- `[FUNDING GOAL]` → Campaign funding goal
- `[DELIVERY TIMELINE]` → Expected delivery timeline

## 📊 State Management

The system maintains processing state in JSON files:

```json
{
  "brand_name": "zack-ai",
  "created_at": "2025-01-14T10:30:00",
  "last_updated": "2025-01-14T11:45:00",
  "completed_templates": ["buyerpersona", "competitor-summary"],
  "current_template": "mds",
  "processing_context": {
    "persona_name": "Tech-Savvy Parent",
    "key_messaging": "AI-powered companion for children"
  },
  "errors": []
}
```

## 🛡 Validation System

### Brand Validation Features:
- **Prohibited Claims**: Prevents medical/therapeutic claims
- **Price Accuracy**: Validates pricing consistency
- **Required Disclaimers**: Ensures compliance content
- **Content Guidelines**: Enforces brand voice and tone

### Validation Process:
1. Content generated with brand context
2. Automated validation against brand requirements
3. Error reporting and prevention of invalid output
4. Context extraction for cross-template consistency

## 📈 Output Structure

Generated files are organized by brand and processing order:

```
output/
└── zack-ai/
    ├── 01_buyerpersona.md
    ├── 02_competitor-summary.md
    ├── 03_product-description.md
    ├── ...
    └── processing_report.md
```

Each file includes:
- Processing metadata (timestamp, brand context)
- Brand-specific content with injected placeholders
- Validation status and compliance notes

## 🔮 Future Enhancements (Phase 2)

### OpenRouter API Integration
The system is architected to support future integration with OpenRouter API for:
- Advanced content generation using multiple LLM providers
- Agentic framework integration
- Real-time content optimization
- A/B testing of generated content

### Planned Features:
- API-driven content generation
- Multi-model content comparison
- Advanced personalization
- Performance analytics integration

## 🐛 Troubleshooting

### Common Issues:

1. **Template Not Found**:
   ```bash
   # Verify template exists
   ls prompt-templates/[template-name].md
   ```

2. **Brand Configuration Error**:
   ```bash
   # Validate configuration
   python crowdfunding_automation.py --validate-brand zack-ai
   ```

3. **State File Corruption**:
   ```bash
   # Remove corrupted state file
   rm state/zack-ai_state.json
   ```

4. **Permission Issues**:
   ```bash
   # Check directory permissions
   chmod 755 output/ state/
   ```

### Logging:
- Default logs: `crowdfunding_automation.log`
- Verbose mode: `--verbose` flag
- Log levels: INFO, ERROR, DEBUG

## 🤝 IDE Integration

### VS Code Integration:
1. Open terminal in VS Code
2. Navigate to project directory
3. Run commands directly in integrated terminal
4. View generated files in explorer panel

### PyCharm Integration:
1. Configure Python interpreter
2. Set working directory to project root
3. Use Run/Debug configurations for different modes
4. Monitor output in console panel

## 📝 Examples

### Complete Workflow Example:
```bash
# 1. Validate brand configuration
python crowdfunding_automation.py --validate-brand zack-ai

# 2. Process all templates
python crowdfunding_automation.py --bulk --brand zack-ai

# 3. View processing report
cat output/zack-ai/processing_report.md
```

### Recovery Example:
```bash
# If processing is interrupted, resume from checkpoint
python crowdfunding_automation.py --resume --brand zack-ai
```

## 📄 License

This project is part of the Zack AI crowdfunding campaign development toolkit.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review log files for error details
3. Validate brand configuration
4. Ensure all dependencies are installed

---

**Note**: This system is designed for the Zack AI crowdfunding campaign but can be adapted for other brands by modifying the `brand_requirements.yaml` configuration file.