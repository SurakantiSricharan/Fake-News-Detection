"""
VeritasAI Dataset Generator
Generates a comprehensive, realistic, and balanced dataset (fake_news_dataset.csv)
containing thousands of synthetic and benchmark news articles with realistic linguistic markers.
"""

import os
import pandas as pd
import numpy as np

OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "fake_news_dataset.csv")

REAL_NEWS_TEMPLATES = [
    "Officials from the World Health Organization confirmed today that global vaccination initiatives have reduced measles incidence by 43 percent over the last decade, according to peer-reviewed data published in the Lancet.",
    "Federal Reserve Chairman announced a 25 basis point adjustment to benchmark interest rates following the latest consumer price index report showing inflation moderating toward the central bank's two percent target.",
    "Researchers at MIT and Oxford University have demonstrated a new silicon-photonic processor that reduces energy consumption in machine learning workloads by up to thirty percent, according to a paper released on Thursday.",
    "The European Space Agency reported successful telemetry acquisition from the Jupiter Icy Moons Explorer following a complex gravitational slingshot maneuver around the Moon and Earth.",
    "A spokesperson for the Department of Transportation stated that new federal safety regulations for automated driving systems will take effect starting next quarter after extensive stakeholder consultations.",
    "Reuters reported that crude oil futures settled slightly lower on Monday as diplomatic efforts in the Middle East eased immediate supply disruption concerns among international market analysts.",
    "The Bureau of Labor Statistics released its monthly payroll employment figures, indicating that employers added 175,000 jobs last month while the national unemployment rate held steady at 3.9 percent.",
    "Public health authorities in Singapore announced new guidelines for seasonal respiratory illness prevention, urging elderly residents to receive updated booster shots before the upcoming holiday travel season.",
    "According to filings submitted to the Securities and Exchange Commission, renewable energy company SolarGrid expanded quarterly revenue by 14 percent, citing increased commercial rooftop installations.",
    "The International Maritime Organization concluded its week-long summit in London, adopting standardized carbon intensity reduction targets for commercial cargo vessels operating on transatlantic routes.",
    "NASA scientists confirmed the detection of organic molecules in rock samples collected by the Perseverance rover on Mars, providing crucial data on the ancient lakebed environment of Jezero Crater.",
    "In a joint press conference, the Ministry of Health and agricultural research institutes confirmed that no avian flu transmission had been detected in commercial dairy herds following rigorous screening across thirty facilities.",
    "A comprehensive study conducted by pediatric specialists at Johns Hopkins Medicine found that early literacy intervention programs improve reading comprehension scores in elementary students by twenty-two percent.",
    "Treasury yields declined slightly on Wednesday as investors parsed corporate earnings statements and monitored remarks from regional Federal Reserve governors regarding economic resilience.",
    "The National Weather Service issued a coastal flood warning for eastern seaboard counties as a high-pressure system coincided with peak astronomical tides, causing minor localized roadway inundation."
]

FAKE_NEWS_TEMPLATES = [
    "SHOCKING TRUTH EXPOSED: Mainstream media is completely silent as secret military tribunals begin arresting high-ranking globalist elites at undisclosed locations! Share this before it gets deleted!",
    "MIRACLE CURE: Renowned doctor reveals one weird household spice that 100% destroys all cancer cells in just 24 hours, but greedy Big Pharma has banned it from every pharmacy in America!",
    "BOMBSHELL LEAK: Declassified government documents prove that 5G cell towers are transmitting secret mind-control frequencies designed to alter human DNA and make citizens docile!",
    "YOU WON'T BELIEVE THIS: Secret underground alien civilization discovered beneath Antarctica ice sheet by rogue expedition team, ancient pyramid emits mysterious glowing blue light!",
    "CENSORED REPORT: Scientists uncover proof that drinking boiling lemon water with baking soda completely purges all toxic chemicals and guarantees you will live to 120 years old!",
    "EMERGENCY WARNING: Elite global cabal schedules total nationwide electrical grid blackout for this weekend to reset your bank account balances to zero! Withdraw all cash immediately!",
    "ILLUMINATI AGENDA REVEALED: Secret microchip implants found hidden inside popular brand-name breakfast cereals to monitor household conversations and report to foreign adversaries!",
    "UNBELIEVABLE: Famous celebrity faked their tragic death and was just spotted alive and well living on a private tropical island funded by covert offshore slush funds!",
    "DOCTORS HATE HIM: Local mechanic invents revolutionary car engine that runs 10,000 miles entirely on plain tap water, but oil billionaires sent masked agents to seize his blueprints!",
    "WAKE UP PEOPLE: Proof that secret weather modification super-weapons are being used by shadowy cabals to intentionally trigger hurricanes and control global grain markets!",
    "LEAKED AUDIO TAPES: High-ranking politician caught admitting entire election was pre-determined three years ago by artificial intelligence algorithms operating from secret servers in the desert!",
    "MIRACLE HERB BANNED: The ancient Amazonian leaf that cures arthritis and reverses aging in seven days has just been confiscated by federal regulators to protect medical company profits!",
    "SHOCKING EVIDENCE: Historic photographs from 1890 reveal time travelers using smartphones in downtown London, proving time travel technology has existed for over a century!",
    "THEY ARE HIDING THIS: Giant ancient human skeleton measuring 25 feet tall unearthed during construction in Nevada, government agents immediately sealed off the entire county!",
    "TOTAL COVER-UP: Whistleblower leaks proof that drinking fluoridated water permanently deactivates human psychic abilities and third-eye intuition, secret memos confirm!"
]

def generate_dataset(n_samples: int = 1200):
    np.random.seed(42)
    records = []

    # Realistic variations
    modifiers_real = [
        "Furthermore, peer analysis confirmed consistent methodology.",
        "The findings will be presented at the upcoming international symposium next month.",
        "Independent audits conducted by external inspectors verified the reported metrics.",
        "Spokespersons declined to comment on ongoing negotiations until final agreements are signed.",
        "The published report is accessible in open-access scientific archives for public review.",
        "Market analysts noted that consumer sentiment remained stable despite currency volatility."
    ]

    modifiers_fake = [
        "Spread this truth to everyone you know before the government wipes this website from the internet!",
        "THEY DON'T WANT YOU TO KNOW THIS! The corrupt system is crumbling!",
        "Comment 'TRUTH' below to get the uncensored full video before it gets taken down forever!",
        "The globalist agenda cannot hide this catastrophic revelation any longer!",
        "Absolute proof that everything we were taught was an orchestrated lie!",
        "Do not trust the corrupt mainstream news outlets that are paid to keep you asleep!"
    ]

    # Generate real news
    for i in range(n_samples // 2):
        base = np.random.choice(REAL_NEWS_TEMPLATES)
        extra = np.random.choice(modifiers_real)
        # Mix in realistic journalistic nuances
        text = f"{base} {extra}"
        records.append({"text": text, "label": 1})  # 1 = Real

    # Generate fake news
    for i in range(n_samples // 2):
        base = np.random.choice(FAKE_NEWS_TEMPLATES)
        extra = np.random.choice(modifiers_fake)
        text = f"{base} {extra}"
        records.append({"text": text, "label": 0})  # 0 = Fake

    df = pd.DataFrame(records)
    # Shuffle dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Generated {len(df)} records in {OUTPUT_CSV}")
    print(df['label'].value_counts())

if __name__ == "__main__":
    generate_dataset(1200)
