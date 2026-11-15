# Deviation request DR-2026-07 · external vision model for inspection photos

**From** Rabah Al-Mujil, lead of the inspections team · **To** the Asas architecture board · **Date** 2026-11-02

**Request.** Allow Kashif to send inspection photos to `ext-vision-q`, an external vision model, for twelve
months, as its primary vision model.

**Why.** `ksa-vision-x` was not admitted: it has no Arabic evaluation evidence, and its provider will publish one
in February 2027 at the earliest. A Ministry-hosted vision model needs a hardware purchase with a nine-month lead
time. Meanwhile inspectors type every report by hand: 14 minutes a report, against about 6 with Kashif's draft.
`ext-vision-q` reads Arabic signs at 0.93 on the Ministry's signage set.

**What we accept.** Photos are classified Restricted because some show faces, car plates or documents. We would
ask inspectors to avoid people in photos.

**Standard affected.** Placement rule P-01: Restricted data may not go to an external host.
