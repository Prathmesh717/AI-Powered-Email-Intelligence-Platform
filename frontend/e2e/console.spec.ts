import { test, expect } from '@testrelic/playwright-analytics/fixture'

test.describe('Smartai console — smoke', () => {
  test('landing page loads', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveTitle(/Smartai/i)
    await expect(page.getByText('Smartai').first()).toBeVisible()
  })

  test('navigates to the architecture page', async ({ page }) => {
    await page.goto('/')
    await page.goto('/architecture')
    await expect(page).toHaveURL(/\/architecture/)
  })
})
