# sam-bedrock-gr-hallucination

## 概要

Knowledge Base for Amazon BedrockにおけるChat with your Document機能と、Guardrails for Amazon Bedrockのcontextual grounding check機能を用いて、RAGの質問・回答・根拠の内容をチェックし、回答にハルシネーションが含まれていないかをチェックするサンプルアプリケーションです。  

## デプロイ手順

1. 以下コマンドでリポジトリをクローンし、ディレクトリを移動

```bash
git clone https://github.com/tsukuboshi/sam-bedrock-gr-apply
cd sam-bedrock-gr-apply
```

2. 以下コマンドで、SAMアプリをビルド

```bash
sam build
```

3. 以下コマンドで、SAMアプリをデプロイ

```bash
sam deploy 
```

4. 以下コマンドで、モデルからの回答として`output.txt`を読み込む設定に変更し、SAMアプリをデプロイ

```bash
sed -i '' 's/"OutputControl=False"/"OutputControl=True"/' samconfig.toml
sam deploy
```

## 参考文献

[Guardrails for Amazon Bedrockのハルシネーション検出\(contextual grounding check\)を試してみた \| DevelopersIO](https://dev.classmethod.jp/articles/guardrails-for-amazon-bedrock-contextual-grounding-check/)
