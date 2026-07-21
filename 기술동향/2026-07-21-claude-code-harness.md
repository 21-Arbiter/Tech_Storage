# [기술동향] LLM 에이전트의 "하네스(Harness)" — Claude Code를 중심으로

## 한 줄 요약
프론티어 모델도 잘 설계된 **하네스(harness)** 없이는 여러 컨텍스트 윈도우에 걸친 긴 에이전틱 작업을 안정적으로 수행하지 못한다. 모델이 "지능"을 제공한다면, 하네스는 그 지능을 통제하고 반복 가능하게 만드는 "제어" 계층이다.

## 하네스란?
- LLM을 감싸서 **툴 사용 방식, 안전 가드레일, 복잡한 작업의 오케스트레이션**을 지시하는 소프트웨어 레이어
- 핵심은 **Thought → Action → Observation (TAO / ReAct) 루프**: 프롬프트 조립 → LLM 호출 → 출력 파싱 → 툴 실행 → 결과를 다시 컨텍스트에 반영 → 반복
- Claude Code의 시스템 프롬프트는 **캐시 경계를 고려한 모듈형 구조**로, 기본 행동 지침 / 툴별 가이드 / 프로젝트 컨텍스트(CLAUDE.md) / 세션 상태 등 여러 세그먼트로 조립됨

## 왜 지금 중요한가
- Anthropic 엔지니어링팀 공식 입장: "에이전트 성능의 병목은 모델이 아니라 하네스 설계"라는 점을 여러 글에서 강조
- 툴 인터페이스 설계 = 에이전트의 UX. 툴 이름/스키마/에러 표면 설계가 에이전트 성능에 직접 영향
- 장시간 실행되는 에이전트일수록 컨텍스트 관리(압축, 서브에이전트 격리, 메모리)가 모델 성능보다 결과를 더 크게 좌우

## 참고자료
**Anthropic 공식**
- [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) — 워크플로우 vs 에이전트, 에이전틱 시스템 설계 원칙의 출발점
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Writing effective tools for AI agents—using AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents)

**커뮤니티/분석**
- [Simon Willison — Highlights from the Claude 4 system prompt](https://simonw.substack.com/p/highlights-from-the-claude-4-system) — 공식 공개 프롬프트 + 유출된 툴 설명까지 주석 정리
- [awesome-harness-engineering (GitHub)](https://github.com/ai-boost/awesome-harness-engineering) — 하네스 엔지니어링 관련 툴/패턴/메모리/MCP/권한/관측성 정리 리스트
- [Dive-into-Claude-Code (GitHub, VILA-Lab)](https://github.com/VILA-Lab/Dive-into-Claude-Code) — Claude Code를 사례로 한 AI 에이전트 시스템 설계 분석

## 메모
- 알리바바 open-code-review 처럼 "에이전트 하이브리드(정확해야 하는 건 엔지니어링 로직, 판단은 에이전트)" 구조가 여러 사례에서 공통적으로 등장하는 패턴으로 보임 → 이후 기술동향에서 개별 사례 비교 예정
