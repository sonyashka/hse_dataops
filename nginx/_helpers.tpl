{{- define "nginx-helm.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "nginx-helm.labels" -}}
helm.sh/chart: {{ include "nginx-helm.chart" . }}
{{ include "nginx-helm.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "nginx-helm.selectorLabels" -}}
app.kubernetes.io/name: {{ include "nginx-helm.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "nginx-helm.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "nginx-helm.image" -}}
{{- printf "%s:%s" .Values.image.repository .Values.image.tag }}
{{- end }}