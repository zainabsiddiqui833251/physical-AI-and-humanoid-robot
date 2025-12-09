// src/components/HomepageFeatures/index.tsx

import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

// Define the structure for a module item
interface ModuleItem {
  title: string;
  description: string;
  link: string;
}

// Data for the modules
const modules: ModuleItem[] = [
  {
    title: 'Foundation of Physical AI & Embodied Intelligence',
    description: 'Explore the foundational ideas behind Physical AI and Humanoid Robotics.',
    link: '/docs/modules/Foundation_of_Physical_AI',
  },
  {
    title: 'ROS 2 Fundamentals',
    description: 'Master the Robot Operating System 2 for building robot software.',
    link: '/docs/modules/ROS_2_Fundamentals',
  },
  {
    title: 'Robot Simulation with Gazebo',
    description: 'Learn to simulate robots and environments using Gazebo.',
    link: '/docs/modules/Robot_stimulation_with_Gazebo',
  },
  {
    title: 'NVIDIA Isaac Platform',
    description: 'Develop AI-powered robots with NVIDIA Isaac SDK and Sim.',
    link: '/docs/modules/NVIDIA_Isaac_platform',
  },
  {
    title: 'Humanoid Robot Development',
    description: 'Dive into kinematics, dynamics, locomotion, and manipulation.',
    link: '/docs/modules/Humanoid_robot_deeveopment',
  },
  {
    title: 'Conversational Robotics',
    description: 'Enable robots to communicate naturally using AI and NLP.',
    link: '/docs/modules/conversational_robotics',
  },
];

// Component to render a single feature card
function Feature({ title, description, link }: ModuleItem) {
  return (
    <div className={clsx('col col--4', styles.feature)}>
      <div
        className={clsx(styles.featureCard)}
        style={{
          backgroundColor: 'var(--ifm-color-white)',
          color: 'var(--ifm-color-dark-gray)',
          borderColor: 'var(--ifm-color-dark-gray)',
        }}
      >
        <div className={styles.featureCardContent}>
          <h3 style={{ color: 'var(--ifm-color-black)' }}>{title}</h3>
          <p>{description}</p>
        </div>
        <div className={styles.featureCardFooter}>
          <Link className={styles.featureLink} to={link}>
            Learn More →
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {   // <-- ❌ removed : JSX.Element
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {modules.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
