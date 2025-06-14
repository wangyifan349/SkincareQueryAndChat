#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

// 最大问题字符串长度（包括结尾的'\0'），用于存储用户输入和字典中的问题
#define MAX_Q_LEN 200
// 答案最大行数，表示每个答案最多可以分成多少行存储
#define MAX_A_LINES 10
// 每行答案字符串最大长度（包括结尾的'\0'），用于存储答案的每一行内容
#define MAX_A_LINE_LEN 200
// 预存Q&A字典条目数量，表示字典中问题-答案对的个数
#define QA_DICT_SIZE 4
// 查询时返回的Top K条目数，表示每次查询最多显示多少条最相关的答案
#define TOP_K 2

// 编辑距离操作的权重定义
// 插入操作的代价
#define COST_INSERT 1
// 删除操作的代价
#define COST_DELETE 1
// 替换操作的代价
#define COST_REPLACE 2


// Q&A字典条目结构体，答案用多行字符串数组存储
typedef struct {
    char question[MAX_Q_LEN];
    char answer_lines[MAX_A_LINES][MAX_A_LINE_LEN];
    int answer_line_count;
} QADictEntry;

// 查询结果结构体，包含字典条目及相似度指标
typedef struct {
    QADictEntry entry;
    int edit_dist;
    int lcs_len;
    double score;  // 综合得分，越小越相关
} ResultEntry;

// 将字符串转换为小写，结果写回原字符串
void to_lowercase(char *str) {
    for (int i = 0; str[i]; i++) {
        str[i] = (char)tolower((unsigned char)str[i]);
    }
}

// 计算最长公共子序列矩阵
void compute_lcs_matrix(const char *X, const char *Y, int L[][MAX_Q_LEN]) {
    int m = (int)strlen(X);
    int n = (int)strlen(Y);
    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= n; j++) {
            if (i == 0 || j == 0)
                L[i][j] = 0;
            else if (X[i - 1] == Y[j - 1])
                L[i][j] = L[i - 1][j - 1] + 1;
            else
                L[i][j] = (L[i - 1][j] > L[i][j - 1]) ? L[i - 1][j] : L[i][j - 1];
        }
    }
}

// 计算加权编辑距离
int weighted_edit_distance(const char *X, const char *Y) {
    int m = (int)strlen(X);
    int n = (int)strlen(Y);
    int D[MAX_Q_LEN][MAX_Q_LEN];
    for (int i = 0; i <= m; i++) D[i][0] = i * COST_DELETE;
    for (int j = 0; j <= n; j++) D[0][j] = j * COST_INSERT;
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (X[i - 1] == Y[j - 1]) D[i][j] = D[i - 1][j - 1];
            else {
                int ins = D[i][j - 1] + COST_INSERT;
                int del = D[i - 1][j] + COST_DELETE;
                int rep = D[i - 1][j - 1] + COST_REPLACE;
                int min = ins;
                if (del < min) min = del;
                if (rep < min) min = rep;
                D[i][j] = min;
            }
        }
    }
    return D[m][n];
}

// 打印查询结果，答案逐行打印
void print_result_entry(ResultEntry *res) {
    printf("问题: %s\n", res->entry.question);
    printf("答案:\n");
    for (int i = 0; i < res->entry.answer_line_count; i++) {
        printf("  %s\n", res->entry.answer_lines[i]);
    }
    printf("最长公共子序列长度: %d\n", res->lcs_len);
    printf("加权编辑距离: %d\n", res->edit_dist);
    printf("综合得分: %.2f\n", res->score);
    printf("--------------------------------------------------\n");
}

// qsort比较函数，按综合得分升序排序
int cmp_score(const void *a, const void *b) {
    ResultEntry *ra = (ResultEntry *)a;
    ResultEntry *rb = (ResultEntry *)b;
    if (ra->score < rb->score) return -1;
    else if (ra->score > rb->score) return 1;
    else return 0;
}

int main() {
    // 预存Q&A字典，答案多行存储
    QADictEntry qa_dict[QA_DICT_SIZE] = {
        {
            "什么是Python？",
            {
                "Python是一种高级编程语言，具有简洁易读的语法。",
                "它支持多种编程范式，包括面向对象、函数式编程等。"
            },
            2
        },
        {
            "如何安装Python？",
            {
                "可以从Python官网下载安装包进行安装，或者使用包管理工具如apt、brew等。",
                "安装完成后，可以在命令行输入python3启动解释器。"
            },
            2
        },
        {
            "Python支持哪些数据类型？",
            {
                "常见的数据类型有：",
                " - 整数(int)",
                " - 浮点数(float)",
                " - 字符串(str)",
                " - 列表(list)",
                " - 字典(dict)",
                "等。"
            },
            7
        },
        {
            "如何定义函数？",
            {
                "使用def关键字定义函数，例如：",
                "def func_name(params):",
                "    # 函数体",
                "    pass"
            },
            4
        }
    };

    char query[MAX_Q_LEN];
    printf("欢迎使用Q&A查询系统！\n");
    printf("请输入问题（输入exit退出）：\n");

    while (1) {
        printf("\n问题: ");
        if (fgets(query, sizeof(query), stdin) == NULL) break;

        // 去除末尾换行符
        size_t len = strlen(query);
        if (len > 0 && query[len - 1] == '\n') query[len - 1] = '\0';

        if (strcmp(query, "exit") == 0) break;

        // 先转换查询字符串为小写
        char query_lower[MAX_Q_LEN];
        strncpy(query_lower, query, MAX_Q_LEN);
        query_lower[MAX_Q_LEN - 1] = '\0';
        to_lowercase(query_lower);

        ResultEntry results[QA_DICT_SIZE];
        int count = 0;

        for (int i = 0; i < QA_DICT_SIZE; i++) {
            // 转换字典问题为小写
            char dict_q_lower[MAX_Q_LEN];
            strncpy(dict_q_lower, qa_dict[i].question, MAX_Q_LEN);
            dict_q_lower[MAX_Q_LEN - 1] = '\0';
            to_lowercase(dict_q_lower);

            int L[MAX_Q_LEN][MAX_Q_LEN];
            compute_lcs_matrix(query_lower, dict_q_lower, L);

            results[count].entry = qa_dict[i];
            results[count].lcs_len = L[strlen(query_lower)][strlen(dict_q_lower)];
            results[count].edit_dist = weighted_edit_distance(query_lower, dict_q_lower);

            // 综合得分计算，alpha权重可调
            double alpha = 1.0;
            results[count].score = results[count].edit_dist - alpha * results[count].lcs_len;

            count++;
        }

        // 按综合得分升序排序
        qsort(results, count, sizeof(ResultEntry), cmp_score);

        int output_num = (count < TOP_K) ? count : TOP_K;
        printf("\nTop %d 相关答案（按综合得分升序排序）：\n", output_num);
        printf("==================================================\n");
        for (int i = 0; i < output_num; i++) {
            print_result_entry(&results[i]);
        }
    }

    printf("程序结束，感谢使用！\n");
    return 0;
}
