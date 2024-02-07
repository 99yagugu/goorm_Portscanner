멀티스레딩 (Multithreading)
---
멀티스레딩은 하나의 프로세스 내에서 여러 개의 스레드를 동시에 실행하는 프로그래밍 기법

스레드(thread)란 프로세스 내에서 독립적으로 실행되는 작은 실행 단위
하나의 프로세스는 여러 개의 스레드로 구성될 수 있으며, 각 스레드는 독립적인 작업을 수행

멀티스레딩을 사용하면 여러 작업을 병렬로 처리하여 프로그램의 응답성을 향상, 다중 코어 CPU를 활용하여 성능을 개선
하지만 스레드 간의 동기화와 공유 데이터에 대한 관리가 필요, 잘못된 사용은 경쟁 조건 및 데드락과 같은 문제를 초래

비동기식 프로그래밍 (Asynchronous Programming)