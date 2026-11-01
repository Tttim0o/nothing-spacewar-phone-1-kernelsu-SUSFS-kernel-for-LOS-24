# Spacewar KSU + SUSFS kernel

Automatický build KernelSU-Next + SUSFS kernelu pre **Nothing Phone (1)** (Spacewar, sm7325, msm-5.4) na **LineageOS 24 (Android 17)**.

## Použitie
1. Záložka **Actions** → **Build Spacewar KSU+SUSFS Kernel** → **Run workflow**.
2. `los_branch`: `lineage-24.0` (over, že vetva existuje pre Spacewar).
3. `stock_boot_url` (nepovinné): odkaz na tvoj stock `boot.img` z LOS 24 zipu.
   Ak ho vyplníš, dostaneš hotový `new-boot.img` na `fastboot flash boot`.
4. Po dobehnutí stiahni artefakt **Spacewar-KSU-SUSFS**.

## Pred flashom
- Stock `boot.img` ber z LOS 24 **zipu** (payload_dumper), nie z telefónu (ten je patchnutý Magiskom).
- Prechádzaš z Magisku na KernelSU → čistý `boot.img` Magisk odstráni.
- Najprv `fastboot boot new-boot.img` (test), až potom `fastboot flash boot new-boot.img`.

## Pozn.
Verzie (clang, Magisk, názov defconfigu) sú odhad — prvý build môže padnúť.
Pri chybe pozri log v Actions a oprav príslušný krok/verziu.
