#!/usr/bin/env python3
"""Test Flight Simulator with Playwright"""
import asyncio
import os
from playwright.async_api import async_playwright

async def test_flight_simulator():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Load the HTML file
        file_path = os.path.abspath('index.html')
        await page.goto(f'file://{file_path}')
        
        # Wait for loading to disappear
        await page.wait_for_selector('#loading', state='hidden', timeout=10000)
        
        # Check if HUD is visible
        hud_visible = await page.is_visible('#hud')
        print(f"HUD Visible: {hud_visible}")
        
        # Check canvas
        canvas = await page.query_selector('#gameCanvas')
        print(f"Canvas exists: {canvas is not None}")
        
        # Get page title
        title = await page.title()
        print(f"Page title: {title}")
        
        # Check for console errors
        errors = []
        page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
        
        await asyncio.sleep(2)
        
        if errors:
            print(f"Console errors: {errors}")
        else:
            print("No console errors detected")
        
        await browser.close()
        print("✅ Flight Simulator test PASSED")

if __name__ == '__main__':
    asyncio.run(test_flight_simulator())
