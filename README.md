# HelloGitHub
First use GItHub
stages:
  - deploy
deploy:
    stage: deploy
    script:
      - deploy Example_Group Example_Project
    only:
      - master
    tags:
      - shell
