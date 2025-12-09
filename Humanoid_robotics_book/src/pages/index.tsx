import React from 'react';
import clsx from 'clsx'; // Helper for conditional class names
import Layout from '@theme/Layout'; // Docusaurus layout component
import Link from '@docusaurus/Link'; // Docusaurus link component
import useDocusaurusContext from '@docusaurus/useDocusaurusContext'; // Hook to access site config
import styles from './index.module.css'; // Page-specific styles

// Import the component that will render the module cards
import HomepageFeatures from '@site/src/components/HomepageFeatures';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <header
      className={clsx('hero hero--primary', styles.heroBanner)}
      style={{
  backgroundColor: 'var(--ifm-color-black)',
  color: 'var(--ifm-color-pale-pink)',
  padding: '6rem 0',
  alignItems: 'center',
}}
    >
      <div className="container">
        <div className="row">
          {/* Left section for text */}
          <div className={clsx('col col--6', styles.heroTextContainer)}>
            <h1
              className={clsx(styles.heroTitle)}
              style={{ color: 'var(--ifm-color-pale-pink)' }}
            >
              {siteConfig.title}
            </h1>
        
            <p
              className={clsx(styles.heroTagline)}
              style={{ color: 'var(--ifm-color-light-pink)' }}
            >
              {siteConfig.tagline}
            </p>
        
            <div className={styles.buttons}>
              <Link
                className="button button--secondary button--lg"
                to="/docs"
                style={{
                  backgroundColor: 'var(--ifm-color-pale-pink)',
                  color: 'white',
                }}
              >
                Explore the Book
              </Link>
            </div>
          </div>
        
          {/* Right section for image */}
          <div className={clsx('col col--6', styles.heroImageContainer)}>
            <img src="/img/img1.png" alt="Hero Image" className={styles.heroImage} />
          </div>
        </div>      </div>
    </header>
  );
}

// ❌ Removed the explicit return type (: JSX.Element)
export default function Home() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Comprehensive guide to Physical AI and Humanoid Robotics"
    >
      <HomepageHeader />

      <main>
        <section
          className={clsx(styles.features, 'padding-vert--md')}
          style={{
            backgroundColor: 'var(--ifm-background-color)',
            color: 'var(--ifm-text-color)',
          }}
        >
          <div className="container">
            <div className="row">
              <div className="col col--12">
                <h2
                  style={{
                    textAlign: 'center',
                    color: 'var(--ifm-heading-color)',
                  }}
                >
                  Key Modules
                </h2>

                <p
                  style={{
                    textAlign: 'center',
                    color: 'var(--ifm-color-secondary)',
                  }}
                >
                  Dive into the core topics covering Physical AI and Humanoid
                  Robotics.
                </p>

                <HomepageFeatures />
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
