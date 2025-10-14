#!/usr/bin/env python3
"""
OpenRouter API Integration Framework for Crowdfunding Automation
Phase 2: Content Generation via Agentic Frameworks

This module provides the foundation for integrating OpenRouter API
to generate actual content from processed templates.
"""

import os
import json
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class OpenRouterConfig:
    """Configuration for OpenRouter API integration"""
    api_key: str
    base_url: str = "https://openrouter.ai/api/v1"
    model: str = "anthropic/claude-3.5-sonnet"
    max_tokens: int = 4000
    temperature: float = 0.7
    timeout: int = 60

@dataclass
class ContentRequest:
    """Request structure for content generation"""
    template_name: str
    prompt: str
    brand_context: Dict[str, Any]
    validation_rules: List[str]
    output_format: str = "markdown"
    priority: int = 1

class OpenRouterClient:
    """Client for OpenRouter API interactions"""
    
    def __init__(self, config: OpenRouterConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.timeout)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def generate_content(self, request: ContentRequest) -> Dict[str, Any]:
        """Generate content using OpenRouter API"""
        if not self.session:
            raise RuntimeError("Client not initialized. Use async context manager.")
            
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://crowdfunding-automation.local",
            "X-Title": "Crowdfunding Campaign Automation"
        }
        
        # Construct the enhanced prompt with brand context
        enhanced_prompt = self._build_enhanced_prompt(request)
        
        payload = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": self._get_system_prompt(request.template_name)
                },
                {
                    "role": "user", 
                    "content": enhanced_prompt
                }
            ],
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "stream": False
        }
        
        try:
            async with self.session.post(
                f"{self.config.base_url}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API request failed: {response.status} - {error_text}")
                
                result = await response.json()
                
                return {
                    "content": result["choices"][0]["message"]["content"],
                    "model": result["model"],
                    "usage": result.get("usage", {}),
                    "timestamp": datetime.now().isoformat(),
                    "template": request.template_name
                }
                
        except Exception as e:
            logger.error(f"Content generation failed for {request.template_name}: {e}")
            raise
    
    def _build_enhanced_prompt(self, request: ContentRequest) -> str:
        """Build enhanced prompt with brand context and validation rules"""
        context_section = self._format_brand_context(request.brand_context)
        validation_section = self._format_validation_rules(request.validation_rules)
        
        return f"""
{request.prompt}

BRAND CONTEXT:
{context_section}

VALIDATION REQUIREMENTS:
{validation_section}

OUTPUT FORMAT: {request.output_format}

Please generate content that:
1. Incorporates all brand context accurately
2. Follows all validation requirements
3. Maintains consistency with the brand voice and positioning
4. Is ready for immediate use in the crowdfunding campaign
"""
    
    def _format_brand_context(self, context: Dict[str, Any]) -> str:
        """Format brand context for prompt injection"""
        formatted = []
        for key, value in context.items():
            if isinstance(value, list):
                formatted.append(f"- {key}: {', '.join(map(str, value))}")
            else:
                formatted.append(f"- {key}: {value}")
        return "\n".join(formatted)
    
    def _format_validation_rules(self, rules: List[str]) -> str:
        """Format validation rules for prompt injection"""
        return "\n".join(f"- {rule}" for rule in rules)
    
    def _get_system_prompt(self, template_name: str) -> str:
        """Get template-specific system prompt"""
        system_prompts = {
            "buyerpersona": "You are an expert marketing analyst specializing in buyer persona development for crowdfunding campaigns.",
            "competitor-summary": "You are a competitive intelligence analyst with expertise in market positioning and differentiation.",
            "product-description": "You are a product marketing specialist focused on compelling product descriptions for crowdfunding.",
            "landingpage-copy": "You are a conversion copywriter specializing in high-converting landing pages for crowdfunding campaigns.",
            "campaign-page-copy": "You are a crowdfunding campaign specialist with expertise in Kickstarter and Indiegogo page optimization.",
            "precampaign-ads-copy": "You are a digital advertising specialist focused on pre-launch campaign acquisition.",
            "default": "You are an expert marketing professional specializing in crowdfunding campaign content creation."
        }
        
        return system_prompts.get(template_name, system_prompts["default"])

class ContentGenerator:
    """High-level content generation orchestrator"""
    
    def __init__(self, openrouter_config: OpenRouterConfig):
        self.config = openrouter_config
        self.generation_queue: List[ContentRequest] = []
        
    def add_request(self, request: ContentRequest):
        """Add content generation request to queue"""
        self.generation_queue.append(request)
        # Sort by priority (higher priority first)
        self.generation_queue.sort(key=lambda x: x.priority, reverse=True)
    
    async def process_queue(self, batch_size: int = 3) -> List[Dict[str, Any]]:
        """Process content generation queue in batches"""
        results = []
        
        async with OpenRouterClient(self.config) as client:
            # Process in batches to avoid rate limiting
            for i in range(0, len(self.generation_queue), batch_size):
                batch = self.generation_queue[i:i + batch_size]
                
                # Process batch concurrently
                tasks = [client.generate_content(request) for request in batch]
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for j, result in enumerate(batch_results):
                    if isinstance(result, Exception):
                        logger.error(f"Failed to generate content for {batch[j].template_name}: {result}")
                        results.append({
                            "template": batch[j].template_name,
                            "error": str(result),
                            "timestamp": datetime.now().isoformat()
                        })
                    else:
                        results.append(result)
                
                # Rate limiting delay between batches
                if i + batch_size < len(self.generation_queue):
                    await asyncio.sleep(2)
        
        return results
    
    def clear_queue(self):
        """Clear the generation queue"""
        self.generation_queue.clear()

class OpenRouterIntegration:
    """Main integration class for Phase 2 implementation"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key required. Set OPENROUTER_API_KEY environment variable.")
        
        self.config = OpenRouterConfig(api_key=self.api_key)
        self.generator = ContentGenerator(self.config)
    
    async def generate_campaign_content(
        self, 
        processed_templates: List[Dict[str, Any]], 
        brand_context: Dict[str, Any],
        validation_rules: List[str]
    ) -> Dict[str, Any]:
        """Generate complete campaign content from processed templates"""
        
        # Create content requests for each processed template
        for template_data in processed_templates:
            request = ContentRequest(
                template_name=template_data["template_name"],
                prompt=template_data["processed_prompt"],
                brand_context=brand_context,
                validation_rules=validation_rules,
                priority=template_data.get("priority", 1)
            )
            self.generator.add_request(request)
        
        # Process all requests
        results = await self.generator.process_queue()
        
        # Organize results by template
        organized_results = {}
        for result in results:
            template_name = result.get("template", "unknown")
            organized_results[template_name] = result
        
        return {
            "campaign_content": organized_results,
            "generation_summary": {
                "total_templates": len(processed_templates),
                "successful": len([r for r in results if "error" not in r]),
                "failed": len([r for r in results if "error" in r]),
                "timestamp": datetime.now().isoformat()
            }
        }

# CLI Integration for Phase 2
def add_openrouter_args(parser):
    """Add OpenRouter-specific arguments to CLI parser"""
    openrouter_group = parser.add_argument_group('OpenRouter Integration (Phase 2)')
    openrouter_group.add_argument(
        '--generate-content', 
        action='store_true',
        help='Generate actual content using OpenRouter API (requires API key)'
    )
    openrouter_group.add_argument(
        '--openrouter-model',
        default='anthropic/claude-3.5-sonnet',
        help='OpenRouter model to use for content generation'
    )
    openrouter_group.add_argument(
        '--batch-size',
        type=int,
        default=3,
        help='Batch size for concurrent content generation'
    )
    openrouter_group.add_argument(
        '--max-tokens',
        type=int,
        default=4000,
        help='Maximum tokens per content generation request'
    )

async def handle_content_generation(args, processed_templates, brand_context, validation_rules):
    """Handle content generation when --generate-content flag is used"""
    if not args.generate_content:
        return None
    
    try:
        integration = OpenRouterIntegration()
        integration.config.model = args.openrouter_model
        integration.config.max_tokens = args.max_tokens
        
        logger.info("Starting content generation with OpenRouter API...")
        results = await integration.generate_campaign_content(
            processed_templates, 
            brand_context, 
            validation_rules
        )
        
        logger.info(f"Content generation completed: {results['generation_summary']}")
        return results
        
    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    async def example():
        # This would be called from the main automation script
        config = OpenRouterConfig(api_key="your-api-key-here")
        
        async with OpenRouterClient(config) as client:
            request = ContentRequest(
                template_name="buyerpersona",
                prompt="Create a detailed buyer persona for our AI companion product...",
                brand_context={"product_name": "Zack AI", "target_audience": "Parents"},
                validation_rules=["No medical claims", "Include privacy disclaimers"]
            )
            
            result = await client.generate_content(request)
            print(json.dumps(result, indent=2))
    
    # Uncomment to run example
    # asyncio.run(example())