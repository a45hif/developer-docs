// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

// const lightCodeTheme = require("prism-react-renderer/themes/github");
// const darkCodeTheme = require("prism-react-renderer/themes/dracula");
const { themes } = require("prism-react-renderer");
const lightTheme = themes.github;
const darkTheme = themes.dracula;

// KaTex stuff
// const math = require("remark-math");
// const katex = require("rehype-katex");
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Bittensor",
  tagline: "Developer Documentation",
  favicon: "img/favicon.ico",
  // Set the production url of your site here
  url: "https://docs.learnbittensor.org",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: "/",
  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "latent-to", // Usually your GitHub org/user name.
  projectName: "developer-docs", // Usually your repo name.
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "throw",
  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".

  customFields: {
    enableIssueLinks: true, // Set to true to enable issue links
    enableEditUrlLinks: true, // Set to true to enable edit url links
    issueBaseUrl: "https://github.com/latent-to/developer-docs/issues",
    enableFeedback: false, // Set to false to disable feedback
  },

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },
  presets: [
    [
      "@docusaurus/preset-classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: "/",
          path: "docs",
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
          sidebarPath: require.resolve("./sidebars.js"),
          sidebarCollapsible: true,
          showLastUpdateTime: true,
          docItemComponent: "@theme/DocItem",
          editUrl: "https://github.com/latent-to/developer-docs/blob/main/",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      }),
    ],
  ],
  plugins: [
    // "@gracefullight/docusaurus-plugin-vercel-analytics",
    [
      "@docusaurus/plugin-client-redirects",
      {
        redirects: [
          {
            to: "/btcli",
            from: "/reference/btcli",
          },
          {
            to: "/staking-and-delegation/delegation",
            from: "/delegation",
          },
          {
            to: "/staking-and-delegation/staking-polkadot-js",
            from: "/staking/staking-polkadot-js",
          },
          {
            to: "/staking-and-delegation/delegation",
            from: "/staking",
          },
          {
            from: "/subnets/register-validate-mine",
            to: "validators/index",
          },
          {
            from: "/recycled-tao",
            to: "/glossary",
          },
          {
            to: "/subnets/walkthrough-prompting",
            from: "/subnets/code-walkthrough-text-prompting",
          },
          {
            to: "/subtensor-nodes",
            from: "/getting-started/running-a-public-subtensor",
          },
          {
            to: "/",
            from: "/subnet-pages",
          },
          {
            to: "/subnets/schedule-coldkey-swap",
            from: "/schedule-key-swap",
          },
          {
            to: "/subnets/schedule-coldkey-swap",
            from: "/subnets/schedule-key-swap",
          },
          {
            to: "/bt-api-ref",
            from: "/reference/bittensor-api-ref",
          },
          {
            to: "/errors",
            from: "/subtensor-nodes/subtensor-error-messages",
          },
        ],
      },
    ],
  ],
  scripts: [
    {
      src: "https://unpkg.com/@antonz/codapi@0.19.10/dist/settings.js",
      defer: true,
    },
    {
      src: "https://unpkg.com/@antonz/codapi@0.19.10/dist/snippet.js",
      defer: true,
    },
  ],
  // clientModules: ["/static/feedbug-widjet.js"],

  stylesheets: [
    {
      href: "https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css",
      type: "text/css",
      integrity:
        "sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM",
      crossorigin: "anonymous",
    },
    {
      href: "https://unpkg.com/@antonz/codapi@0.19.10/dist/snippet.css",
    },
  ],
  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: "img/bittensor-dev-docs-social-card.png",
      docs: {
        sidebar: {
          autoCollapseCategories: true,
          hideable: false,
        },
      },

      // announcementBar: {
      //   id: 'support_us',
      //   content:
      //     'The dynamic TAO docs are preliminary. Check <a target="_blank" rel="noopener noreferrer" href="#">this page for more.</a>',
      //   backgroundColor: '#171717',
      //   textColor: '#f43228',
      //   isCloseable: false,
      // },

      navbar: {
        logo: {
          alt: "Bittensor",
          src: "img/logo.svg",
          srcDark: "img/logo-dark-mode.svg",
          href: "https://learnbittensor.org",
          style: {
            objectFit: "contain",
            width: 21,
          },
        },
        items: [
          {
            position: "left",
            label: "What is Bittensor?",
            to: "learn/introduction",
          },
          {
            position: "left",
            label: "SubtensorAPI",
            to: "sdk/subtensor-api",
          },
          {
            position: "left",
            label: "Bittensor SDK Reference",
            to: "bt-api-ref",
          },
          {
            position: "left",
            label: "BTCLI Live Coding Playground",
            to: "btcli/btcli-playground",
          },

          {
            position: "left",
            label: "EVM on Bittensor",
            to: "evm-tutorials",
          },
          {
            type: "search",
            position: "left",
            className: "custom_algolia",
          },
          {
            to: "bittensor-rel-notes",
            label: "Releases",
            position: "left",
          },
          {
            href: "https://github.com/latent-to/developer-docs",
            label: "Docs GitHub",
            position: "right",
          },
        ],
      },

      prism: {
        theme: lightTheme,
        darkTheme: darkTheme,
        additionalLanguages: ["bash", "python", "diff", "json", "yaml"],
      },
      algolia: {
        appId: "UXNFOAH677",
        apiKey: "72af66272aba6bd27e76ac6f7eec0068",
        indexName: "learnbittensor",
        contextualSearch: true,
        insights: true,
        debug: false,
        searchPagePath: "search",
        // // Optional: Replace parts of the item URLs from Algolia. Useful when using the same search index for multiple deployments using a different baseUrl. You can use regexp or string in the `from` param. For example: localhost:3000 vs myCompany.com/docs
        // replaceSearchResultPathname: {
        //   from: "/docs/", // or as RegExp: /\/docs\//
        //   to: "/",
        // },
      },
      footer: {
        copyright: `
					<div className="copyRight">
						© ${new Date().getFullYear()} <a href="https://learnbittensor.org">LearnBittensor</a> • <a href="https://latent.to/">Latent Holdings</a>, <span>all rights reserved.</span>
            <a href="mailto:m@latent.to">contact the docs team</a>
          </div>
					<a href='https://learnbittensor.org/'>
					<img src="img/logo-dark-mode.svg" alt="logo"/>
					</a>
				`,
      },
    }),
};

module.exports = config;
