# Sample workflow for building and deploying a Jekyll site to Cloudflare Pages
name: Deploy Jekyll with cloudflare Pages dependencies preinstalled

on:
  # Runs on pushes targeting the default branch
  push:
    branches: ["master"]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:
    
permissions:
  contents: read
  pages: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: Build with Jekyll
        uses: actions/jekyll-build-pages@v1
        with:
          source: ./
          destination: ./_site
      - name: replace path
        run: |
          REPO_NAME=$(echo ${{ github.repository }} | cut -d'/' -f2)
          echo "Repository Name: $REPO_NAME"
          pwd
          ls -la
          sudo sed -i 's/\/href=\"\/$REPO_NAME/href=\"/g' ./_site/index.html
#          cat ./_site/index.html
      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: iptv
          directory: _site
          wranglerVersion: '3'