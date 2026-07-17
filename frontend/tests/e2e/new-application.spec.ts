import { expect, test } from "@playwright/test";

test("new application page renders required form fields", async ({
  page,
}) => {
  await page.goto("/applications/new");

  await expect(
    page.getByRole("heading", {
      name: "Add a job application",
    }),
  ).toBeVisible();

  await expect(page.getByLabel("Company")).toBeVisible();

  await expect(page.getByLabel("Position title")).toBeVisible();

  await expect(page.getByLabel("Location")).toBeVisible();

  await expect(page.getByLabel("Status")).toBeVisible();

  await expect(page.getByLabel("Job posting URL")).toBeVisible();

  await expect(page.getByLabel("Job description")).toBeVisible();

  await expect(page.getByLabel("Notes")).toBeVisible();

  await expect(
    page.getByRole("button", {
      name: "Create application",
    }),
  ).toBeVisible();
});

test("new application form shows client-side required-field error", async ({
  page,
}) => {
  await page.goto("/applications/new");

  await page
    .getByRole("button", {
      name: "Create application",
    })
    .click();

  await expect(page.getByLabel("Company")).toBeFocused();
});