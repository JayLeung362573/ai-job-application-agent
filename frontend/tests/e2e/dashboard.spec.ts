import { expect, test } from "@playwright/test";

test("dashboard renders core application tracking UI", async ({
  page,
}) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", {
      name: "Job Application Tracker",
    }),
  ).toBeVisible();

  await expect(
    page.getByRole("link", {
      name: "Add application",
    }),
  ).toBeVisible();

  await expect(
    page.getByRole("heading", {
      name: "Applications",
    }),
  ).toBeVisible();

  await expect(
    page.getByRole("searchbox", {
      name: "Search applications",
    }),
  ).toBeVisible();

  await expect(
    page.getByLabel("Filter by status"),
  ).toBeVisible();
});

test("dashboard search form preserves query in the URL", async ({
  page,
}) => {
  await page.goto("/");

  await page
    .getByRole("searchbox", {
      name: "Search applications",
    })
    .fill("python");

  await page
    .getByLabel("Filter by status")
    .selectOption("APPLIED");

  await page
    .getByRole("button", {
      name: "Apply filters",
    })
    .click();

  await expect(page).toHaveURL(/q=python/);
  await expect(page).toHaveURL(/status=APPLIED/);
});