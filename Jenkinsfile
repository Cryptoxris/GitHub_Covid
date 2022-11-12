pipeline {
  agent any
  stages {
    stage('error') {
      steps {
        build(job: 'GitHub_Covid', quietPeriod: 10, wait: true)
      }
    }

  }
}