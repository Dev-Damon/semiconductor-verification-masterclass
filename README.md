# 반도체 검증 마스터클래스 · Semiconductor Verification Masterclass

> 소프트웨어 개발자의 직관을 **반도체 검증(Design Verification) 엔지니어의 언어**로 번역하는 PPT형 강의 자료.
> 비유 · 다이어그램 · 면접 답변까지, 한 챕터씩 정복하는 다크 테크 슬라이드 덱.

🔗 **온라인으로 보기 → https://dev-damon.github.io/semiconductor-verification-masterclass/**

---

## 무엇인가요?

DV/SoC 검증 직무의 핵심 키워드를, 반도체 전공 지식이 없는 개발자도 이해할 수 있게 풀어쓴 **19챕터 · 약 220장**의 슬라이드 강의입니다. 모든 페이지는 외부 의존성 없이 동작하며(오프라인 OK), `←` `→` 또는 `Space`로 넘깁니다.

## 커리큘럼

| Part | 내용 |
|------|------|
| **0. 기초 다리** | 반도체·칩·SoC란 / 디지털 회로 복습 / 검증이란 무엇인가 |
| **1. 설계 언어** | Verilog / SystemVerilog |
| **2. 검증 방법론** | UVM / C-test vs UVM-test 환경 |
| **3. 칩 내부 통신** | AMBA APB / AXI / Cache Coherency |
| **4. 시뮬레이션** | Compile·Elaboration·Simulation 3단계 / Xcelium·VCS / Gate-Level Sim & Timing |
| **5. SoC·전력** | SoC Booting Flow / DVFS / UPF Power-Aware Sim & Emulation |
| **6. 테스트·DFT** | JTAG·iJTAG·JTAG2APB / MBIST·Scan·IST·POST |
| **7. 협업 도구** | Git in 하드웨어 팀 |

## 로컬에서 보기

저장소를 내려받아 `index.html`을 브라우저로 열면 됩니다. (별도 빌드·서버 불필요)

```
index.html            ← 목차 허브에서 시작
assets/style.css      ← 공용 다크 테크 디자인
assets/slides.js      ← 슬라이드 엔진(키보드 ←/→, Space)
chapters/chX-Y.html   ← 각 챕터
```

## 특징

- 🎯 챕터마다 **면접 예상 Q&A**와 **핵심 한 줄** 정리
- 💡 모든 개념을 일상 비유와 그림으로 직관적으로 풀이
- 🖼️ 인라인 SVG 다이어그램 · 비교표 · 비유 박스
- 🌙 다크 테크 톤, 의존성 0 (오프라인 동작)

---

*학습용 자료입니다. 내용은 개념 이해·면접 대비 수준을 목표로 작성되었습니다.*
