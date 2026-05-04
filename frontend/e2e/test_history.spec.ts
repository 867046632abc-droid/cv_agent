import { test, expect } from "@playwright/test";

test("history page shows records", async ({ page }) => {
  await page.route("/api/analysis/history", (r) =>
    r.fulfill({
      json: [
        { analysis_id: 1, jd_preview: "We need a Python engineer...", score: 85, status: "done", created_at: new Date().toISOString() },
      ],
    })
  );

  await page.goto("/history");
  await expect(page.locator("text=We need a Python engineer...")).toBeVisible();
  await expect(page.locator("text=85")).toBeVisible();
});

test("history page shows empty state", async ({ page }) => {
  await page.route("/api/analysis/history", (r) => r.fulfill({ json: [] }));
  await page.goto("/history");
  await expect(page.locator("text=暂无分析记录")).toBeVisible();
});
