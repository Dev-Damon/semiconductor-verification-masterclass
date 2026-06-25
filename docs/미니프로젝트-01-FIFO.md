# 미니프로젝트 ① — 동기 FIFO 설계 + 검증

> [학습 로드맵](학습-로드맵.md) **Phase 2(HDL)**의 첫 핸즈온. 환경은 [실습환경-셋업](실습환경-셋업.md) 참고.
> 목표: "RTL을 직접 짜고, **테스트벤치로 버그를 잡는다**"는 검증의 본질을 처음부터 끝까지 경험.

FIFO를 고른 이유: 검증 입문의 **표준 예제**다. 조합/순차, 포인터, full/empty 경계조건, 동시 read/write 등 검증 포인트가 풍부하고, 면접 단골이다.

---

## 0. 단계별 진행 (Phase 2 2주에 맞춤)

| 랩 | 산출물 | 도구 | 배우는 것 |
|---|---|---|---|
| **랩1** | 4-bit 카운터 + TB | iverilog+GTKWave | 시뮬/파형 흐름 익히기(워밍업) |
| **랩2** | **동기 FIFO RTL** | iverilog | 순차회로·포인터·플래그 |
| **랩3** | FIFO **Verilog 방향성 TB** | iverilog+GTKWave | 자극·기대값·경계조건 |
| **랩4** | FIFO **SystemVerilog 랜덤 TB + SVA + 커버리지** | EDA Playground | constrained-random·assertion·coverage |

랩4까지가 **미니프로젝트 ①**. 결과물은 Git에 정리(= 포트폴리오 씨앗).

---

## 1. 사양 (Synchronous FIFO)

단일 클럭 동기 FIFO. 파라미터화.

| 파라미터 | 기본값 | 의미 |
|---|---|---|
| `DATA_WIDTH` | 8 | 데이터 비트폭 |
| `DEPTH` | 16 | 엔트리 수(2의 거듭제곱) |

### 포트
| 신호 | 방향 | 폭 | 설명 |
|---|---|---|---|
| `clk` | in | 1 | 클럭 |
| `rst_n` | in | 1 | 비동기/동기 리셋(active-low) |
| `wr_en` | in | 1 | 쓰기 요청 |
| `din` | in | DATA_WIDTH | 입력 데이터 |
| `rd_en` | in | 1 | 읽기 요청 |
| `dout` | out | DATA_WIDTH | 출력 데이터 |
| `full` | out | 1 | 가득 참 |
| `empty` | out | 1 | 비어 있음 |
| `count` | out | $clog2(DEPTH)+1 | (선택) 현재 적재 수 |

### 동작 규칙
- `wr_en & !full` → `din`을 write 포인터 위치에 저장, wr_ptr++.
- `rd_en & !empty` → rd_ptr 위치 데이터를 `dout`으로, rd_ptr++.
- `full`일 때 write 무시, `empty`일 때 read 무시(언더/오버플로 금지).
- 동시 read+write(full도 empty도 아닐 때)는 둘 다 정상 수행.
- 리셋 시 포인터·플래그 초기화(empty=1, full=0).

> 구현 힌트: 깊이가 2^n이면 **n+1비트 포인터**로 wrap 비트까지 비교해 full/empty 구분(고전 기법). 또는 `count` 레지스터로 판단(더 쉬움 — 입문엔 이쪽 권장).

---

## 2. 검증 포인트 (꼭 테스트할 시나리오)

방향성 테스트(랩3)에서 아래를 **순서대로** 확인:
1. 리셋 직후 `empty==1`, `full==0`.
2. 1개 write → empty 풀림. 1개 read → 값 일치 + 다시 empty.
3. **가득 채우기**(DEPTH번 write) → 마지막에 `full==1`.
4. full 상태에서 추가 write → **무시되는지**(데이터 안 깨지는지).
5. **전부 빼기** → 순서(FIFO=선입선출) 정확? 마지막에 `empty==1`.
6. empty 상태에서 read → 무시되는지.
7. 동시 read+write 반복 → 데이터 정합성.
8. (랜덤, 랩4) wr_en/rd_en 랜덤 토글 수천 사이클 → 레퍼런스 모델과 불일치 0.

### 셀프 체크 모델(스코어보드)
TB 안에 **소프트웨어 큐**(SV `queue` 또는 cocotb `list`)를 두고, DUT에 push할 때 큐에도 push, pop할 때 큐 front와 `dout` 비교 → 불일치 시 에러. *이게 스코어보드의 원형이고, UVM scoreboard로 그대로 확장된다.*

---

## 3. SystemVerilog Assertion (랩4)

면접에서 "SVA 써봤냐"는 단골. 최소 3개:
```systemverilog
// 1) full일 때 write 들어와도 count 안 늘어남
assert property (@(posedge clk) disable iff(!rst_n)
  (full && wr_en && !rd_en) |=> (count == $past(count)));
// 2) empty면 dout 유효치 않음 / read 무시
assert property (@(posedge clk) disable iff(!rst_n)
  (empty && rd_en && !wr_en) |=> (count == $past(count)));
// 3) full과 empty가 동시에 1이면 안 됨
assert property (@(posedge clk) disable iff(!rst_n) !(full && empty));
```

### 커버리지(랩4)
- `full`==1 도달, `empty`==1 도달, 동시 read+write 발생 각각 covered.
- `count`가 0~DEPTH 전 구간을 거쳤는지(covergroup bins).

---

## 4. 완료 기준(Definition of Done)

- [ ] FIFO RTL이 합성가능 스타일(`always_ff`/`always @(posedge clk)`)로 작성됨
- [ ] 방향성 TB로 위 시나리오 1~7 통과, GTKWave 파형으로 full/empty 전이 확인
- [ ] SV 랜덤 TB가 스코어보드로 수천 사이클 자동 검증, **불일치 0**
- [ ] SVA 3개 통과, 커버리지 항목 100%
- [ ] **일부러 버그를 심어**(예: full 조건 `>`→`>=` 오류) TB가 그 버그를 **잡는지** 확인 ← 검증의 핵심 역량 증명
- [ ] Git 저장소에 RTL/TB/파형/README 정리

> **포트폴리오 팁:** README에 "검증 시나리오 표 + 심은 버그를 TB가 잡은 로그 + 커버리지 캡처"를 넣으면, 신입 검증 지원에서 강력한 증거가 된다.

---

## 5. 다음 단계

FIFO를 SV/UVM로 끝냈다면 → **Phase 3 미니프로젝트 ②: APB 슬레이브 레지스터 블록 UVM 환경**으로 확장. (driver/monitor/scoreboard/agent를 FIFO에서 배운 스코어보드 개념 위에 얹는다.)
