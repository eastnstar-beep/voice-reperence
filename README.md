# 외형 평가자 사이트

스마트폰에서는 질의/후보를 세로로 보고 이미지를 탭해 확대합니다. 큰 점수·Useful 버튼을 선택하면 자동 저장되며 하단에서 이전/다음과 진행률을 확인합니다. 언제든 중단하고 이어갈 수 있습니다. 미완성 선택은 같은 브라우저에 임시 저장되지만 JSON에는 완성된 평점만 포함합니다.

척도는 1~5입니다. 1: 거의 비슷하지 않음 / 외형적 공통점이 거의 없음. 2: 일부 특징만 비슷함. 3: 전체적으로 어느 정도 비슷함. 4: 상당히 비슷함. 5: 매우 비슷하며 좋은 외형 레퍼런스로 볼 수 있음. Useful은 독립적인 판단입니다. 미평가는 점수 없이 남으며 JSON에 rating_scale={min:1,max:5}를 포함합니다.

이 폴더만 별도 repository에 올립니다. 관리자 파일·원본 프로젝트를 추가하지 마세요.

1. GitHub에서 새 빈 repository를 만들고 기본 branch를 main으로 둡니다.
2. 이 폴더의 내용을 repository 루트에 push합니다. 숨겨진 .github 폴더도 포함합니다.
3. Settings → Pages → Build and deployment → Source를 GitHub Actions로 설정합니다.
4. Actions의 Deploy evaluator site가 완료되면 Settings → Pages 또는 github-pages deployment에서 URL을 확인합니다. 일반적으로 https://사용자명.github.io/저장소명/ 입니다.

빌드는 Python 표준 라이브러리만 사용합니다: `python scripts/build.py`. site에서 평가자 파일만 dist로 복사하고 공개 내용 검사를 통과해야 배포합니다. 이미지 상대 경로는 repository subpath에서 동작합니다. dist에 오래된 파일이 있으면 검사가 실패하므로 생성한 dist만 정리하고 다시 빌드합니다.

평가자는 URL을 열어 이미지를 평가하고 저장합니다. 계정은 필요 없습니다. 진행상황은 localStorage에만 보관됩니다. 중간/완료 결과 JSON을 다운로드해 프로젝트 소유자에게 직접 전달하세요. 자동 결과 수집은 없습니다. 브라우저 저장소 삭제·기기 변경 시 다운로드한 JSON으로 이어갈 수 있습니다.

공개 파일은 site/index.html, site/images/*.png, site/.nojekyll입니다. scripts/build.py, 이 안내, workflow는 repository 설정용이며 웹 배포에는 포함하지 않습니다. 평점·개인 DB·관리자 매핑은 이 repository에 넣지 마세요. 이미지 자료는 직접 제작한 CC0 합성 자료입니다.
