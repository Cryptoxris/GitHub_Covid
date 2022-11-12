pipeline {
  agent any
  stages {
    stage('error') {
      steps {
        build(job: 'covid', quietPeriod: 10, wait: true)
      }
    }

  }
}