import { test, expect } from "@playwright/test";

test.beforeEach(async ({ page, context }) => {
  await context.grantPermissions(["clipboard-read", "clipboard-write"]);
  await page.route("/api/analysis/1/status", (r) =>
    r.fulfill({ json: { analysis_id: 1, status: "done", progress_label: "分析完成" } })
  );
  await page.route("/api/analysis/1/result", (r) =>
    r.fulfill({
      json: {
        analysis_id: 1, status: "done",
        jd_profile: { hard_requirements: [], nice_to_have: [], responsibilities: [], culture_signals: [], role_tags: [], reasoning: "" },
        match_report: { score: 80, strengths: [], gaps: [], reasoning: "" },
        interview_questions: { technical: [], project: [], gap: [] },
        intro_zh: "这是一段中文自我介绍",
        intro_en: "This is an English self-introduction",
      },
    })
  );
});

test("copy intro to clipboard", async ({ page }) => {
  await page.goto("/analysis/1");
  await page.click("text=自我介绍");
  await page.click("text=复制");

  const clipboardText = await page.evaluate(() => navigator.clipboard.readText());
  expect(clipboardText.length).toBeGreaterThan(0);
});
