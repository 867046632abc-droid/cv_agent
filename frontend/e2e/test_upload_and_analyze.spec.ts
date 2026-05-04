import { test, expect } from "@playwright/test";
import path from "path";

const MOCK_RESULT = {
  analysis_id: 1,
  status: "done",
  jd_profile: {
    hard_requirements: ["Python", "LangGraph"],
    nice_to_have: ["Docker"],
    responsibilities: ["Build AI systems"],
    culture_signals: ["Fast-paced"],
    role_tags: ["Agent"],
    reasoning: "ok",
  },
  match_report: {
    score: 85,
    strengths: ["Strong LangGraph experience"],
    gaps: [{ gap: "TypeScript", mitigation: "Highlight transferable skills" }],
    reasoning: "Good match",
  },
  interview_questions: {
    technical: [{ question: "Explain LangGraph state.", hint: "Focus on StateGraph." }],
    project: [{ question: "Walk me through your RAG system.", hint: "Mention RAGAS." }],
    gap: [{ question: "TypeScript experience?", hint: "Mention JS background." }],
  },
  intro_zh: "你好，我是程云杨，专注于LLM应用开发...",
  intro_en: "Hello, I am Cheng Yunyang, focused on LLM application development...",
};

test.beforeEach(async ({ page }) => {
  await page.route("/api/resume/upload", (route) =>
    route.fulfill({ json: { resume_id: 1, filename: "resume.pdf" } })
  );
  await page.route("/api/analysis/start", (route) =>
    route.fulfill({ json: { analysis_id: 1 } })
  );
  await page.route("/api/analysis/1/status", (route) =>
    route.fulfill({ json: { analysis_id: 1, status: "done", progress_label: "分析完成" } })
  );
  await page.route("/api/analysis/1/result", (route) =>
    route.fulfill({ json: MOCK_RESULT })
  );
});

test("upload PDF and start analysis navigates to result page", async ({ page }) => {
  await page.goto("/");

  const pdfPath = path.join(__dirname, "fixtures", "sample.pdf");
  const [fileChooser] = await Promise.all([
    page.waitForEvent("filechooser"),
    page.click("text=拖拽 PDF 到此处"),
  ]);
  await fileChooser.setFiles(pdfPath);

  await page.fill("textarea", "We are looking for a Python LangGraph engineer with 2+ years experience in AI application development.");
  await page.click("text=开始 AI 分析");

  await page.waitForURL(/\/analysis\/1/);
  await expect(page.locator("text=85")).toBeVisible();
});
