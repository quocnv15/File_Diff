# 📜 Frontend Scripts Documentation

## Overview
This document describes all frontend JavaScript components.

---

## main
**File:** `frontend/scripts/main.js`

18: * File handling functions
20:function handleFileSelect(fileNumber, input) {
57:function checkFilesReady() {
74: * Drag and drop functionality
76:function initializeDragAndDrop() {

---

## api integration
**File:** `frontend/scripts/api_integration.js`

37:async function apiRequest(url, options = {}) {
59:async function uploadFile(file) {
83:async function processFile(fileId, fileName) {
111:async function compareFilesApi(file1Id, file2Id, options = {}) {
137: * Backend connection functions

---

## diff-visualization
**File:** `frontend/scripts/diff-visualization.js`

19:function switchDiffView(viewType) {
68:function generateSideBySideDiff(data1, data2) {
109:function generateUnifiedDiff() {
130:function createDiffLine(content, lineNumber, type, highlights = null) {
163:function createUnifiedDiffLine(comparison) {

---

