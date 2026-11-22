# Netheretヘルプデスク ステップ16：完成版

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [日本語](README.ja.md) | [Deutsch](README.de.md)

授業のための作例です。16のステップで、小さな会社のITを支える架空の会社Netheretのために、ヘルプデスクのWebアプリを作ってきました。これが完成したアプリで、変更履歴、参考資料、テストログが付いています。

## アプリでできること

| 役割 | できること |
|------|------------------|
| 顧客 | サポート依頼を登録する、自分の会社の依頼をタイムラインで追う、コメントを加える、ナレッジベースを読む |
| Tier 1のエージェント | キューを振り分ける、依頼を割り当てたりエスカレーションしたりする、内部向けか顧客に見える更新を加える、顧客の代わりに依頼を記録する、ナレッジベースを使って書く |
| Tier 2 / Tier 3のエンジニア | エスカレーションされた依頼を引き受けて対応する、自分の予定を見る、作業指示書を読んで進み具合を記録する |
| マネージャー | スタッフができることすべてに加えて、誰にでも割り当てる、訪問作業を予定に入れる、レポートを見る |

誰でもSettingsで大きな文字とハイコントラストを選べます。

## 動かしてみる

Python 3.10以降が必要です。

```
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
flask --app helpdesk run --debug
```

http://127.0.0.1:5000 を開きます。`python seed.py` は、実行するたびにすべてを削除して、
新しいサンプルデータを読み込みます。

### デモ用アカウント

どれもデモ用パスワード `password123` を使います。これはこのサンプル
データ専用です。

| 役割 | メールアドレス |
|------|-------|
| マネージャー | `manager@netheret.example` |
| Tier 1 | `tier1@netheret.example` |
| Tier 2 | `tier2@netheret.example` |
| Tier 3 | `tier3@netheret.example` |
| 顧客（Brightwell Bakery） | `customer@brightwell.example` |
| 顧客（Harbour Dental Practice） | `customer@harbour.example` |

### 本番のサーバーでは

`SECRET_KEY` に長くてランダムな値を設定し、HTTPSの背後では `SESSION_COOKIE_SECURE=1` を
設定してください。そして `flask run` ではなく、本番用のWebサーバーでアプリを動かします。
`SECRET_KEY` がないと、アプリは起動のたびにランダムな鍵を作ります。自分のコンピューターなら
それで問題ありません。

## コードの構成

```
requirements.txt       Flask and Flask-SQLAlchemy, pinned
seed.py                sample data (deletes everything first)
helpdesk/
  __init__.py          create_app(): settings and blueprints
  extensions.py        the db object
  models.py            the six tables and the allowed values
  auth.py              sign in and out, login_required, role_required
  security.py          CSRF token and security headers
  main.py              home, dashboard, privacy, error pages
  tickets.py           raise, queue, detail, assign, escalate, updates
  customer.py          the customer's requests and comments
  jobs.py              scheduling, week view, my schedule, job briefs
  articles.py          the knowledge base
  reports.py           KPIs for managers
  settings.py          accessibility settings
  filters.py           how dates are shown
  templates/           Jinja templates, one folder per feature
  static/css/style.css all the styles
  static/js/charts.js  bar charts drawn from the report tables
docs/
  test-log.md          fifty manual tests and their results
  change-log.md        what each step changed, and why
  sources.md           what came from where, and the use of AI
```

## 画面録画のための短いデモ

1. Brightwellの顧客としてサインインし、依頼を登録します。
2. Tier 1としてサインインし、キューでその依頼を見つけ、関連する記事を読んでから、
   理由を添えてTier 2へエスカレーションします。
3. マネージャーとしてサインインし、Sam Okaforに割り当てて、訪問を予定に入れます。
4. Tier 2としてサインインし、My scheduleを開いて作業指示書を読み、完了にします。
5. 顧客に戻ると、タイムラインには訪問が表示されますが、内部メモは
   表示されません。
6. マネージャーとしてReportsを開きます。それから大きな文字とハイコントラストをオンにします。

## 注目するところ

- `docs/test-log.md`：何をテストし、何が失敗し、どう直したか。
- `docs/sources.md`：それぞれのパターンをどのドキュメントから取ったか、そして
  AIが書いたコードを確かめたあと何を変えたか。
- `git log --oneline` と `git checkout step-07`（どのステップでも）を実行すると、
  その時点のアプリを見られます。`git checkout main` で戻ります。

## このステップを学ぶ

これは **Task 2. Developing the solution** の16ステップ中のステップ16です。T Level Digital Software Developmentの無料レッスン（英語）のシリーズで、PythonとFlaskを使い、アジャイルのスプリントでNetheretのヘルプデスクを作ります。このステップのレッスンはこちらです：
[変更履歴、参考資料、完成したアプリ](https://mitsurutech.co.uk/resources/t-level/dsd-t2-16-final)。

- 前のステップ：[ステップ15「手作業のテストとテストログ」](https://github.com/mitsurutech/netheret-helpdesk-15-test-log)
- [T Level Digitalの無料レッスン一覧](https://mitsurutech.co.uk/resources/t-level)
- [これらのレッスンをMitsuruTechでクラスに教える](https://mitsurutech.co.uk/ja/learning)、[料金を見る](https://mitsurutech.co.uk/ja/pricing)、
  [学校で無料の1年を始める](https://mitsurutech.co.uk/ja/signup)

## この作例について

T Level Digital Software Developmentの授業のための作例として、[Mitsuru Technologies](https://mitsurutech.co.uk/ja)（MitsuruTech）が書きました。
Netheret IT Support Solutionsの課題文はPearsonのサンプル評価資料によるものです。このコードと解説は私たち自身のもので、
PearsonやDepartment for Educationが公開、推奨、承認したものではありません。
「T Level」はDepartment for Educationの登録商標です。
