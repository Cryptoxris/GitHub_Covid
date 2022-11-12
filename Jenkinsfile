pipeline {
  agent any
  stages {
    stage('error') {
      steps {
        build(job: 'Covid', quietPeriod: 10, wait: true)
      }
    }

  }
}
