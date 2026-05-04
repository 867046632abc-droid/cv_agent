import { test, expect } from "@playwright/test";

const MOCK_RESULT = {
  analysis_id: 1, status: "done",
  jd_profile: { hard_requirements: ["Python"], nice_to_have: [], responsibilities: [], culture_signals: [], role_tags: [], reasoning: "" },
  match_report: { score: 78, strengths: ["Python expertise"], gaps: [{ gap: "TypeScript", mitigation: "Highlight JS" }], reasoning: "" },
  interview_questions: {
    technical: [{ question: "Explain async/await in Python.", hint: "Focus on event loop." }],
    project: [{ question: "Describe your RAG system.", hint: "Mention evaluation." }],
    gap: [{ question: "TypeScript experience?", hint: "Mention transfer." }],
  },
  intro_zh: "中文自我介绍内容测试",
  intro_en: "English self-introduction content test",
};

test.beforeEach(async ({ page }) => {
  await page.route("/api/analysis/1/status", (r) =>
    r.fulfill({ json: { analysis_id: 1, status: "done", progress_label: "分析完成" } })
  );
  await page.route("/api/analysis/1/result", (r) => r.fulfill({ json: MOCK_RESULT }));
});

test("result page tabs switch correctly", async ({ page }) => {
  await page.goto("/analysis/1");
  await expect(page.locator("text=优势项")).toBeVisible();

  await page.click("text=面试题");
  await expect(page.locator("text=技术深挖")).toBeVisible();

  await page.click("text=自我介绍");
  await expect(page.locator("text=中文自我介绍内容测试")).toBeVisible();
});
