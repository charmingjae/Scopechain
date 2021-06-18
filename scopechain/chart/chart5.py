import matplotlib.pyplot as plt
import numpy as np


# xlabel
cycle = ['1 thread/process', '2 threads/processes', '5 threads/processes']

# Thread Data
simul1_avg = 0.61
simul2_avg = 0.42
simul3_avg = 0.31

# Process Data
proc1_avg = 2.88
proc2_avg = 5.80
proc3_avg = 9.80


def main():

    def compute_pos(xticks, width, i, models):
        index = np.arange(len(xticks))
        n = len(models)
        correction = i-0.5*(n-1)
        return index + width*correction

    def present_height(ax, bar):
        for rect in bar:
            height = rect.get_height()
            posx = rect.get_x()+rect.get_width()*0.5
            posy = height*1.01
            ax.text(posx, posy, '%.3f' %
                    height, rotation=90, ha='center', va='bottom')
    # model
    models = ['Multithread', 'Multiprocess']
    # set xticks
    xticks = ['1 thread/process', '2 threads/processes', '5 threads/processes']
    data = {'Multithread': [0.61, 0.42, 0.31],
            'Multiprocess': [2.88, 5.80, 9.80]}

    # 2. matplotlib의 figure 및 axis 설정
    # 1x1 figure matrix 생성, 가로(7인치)x세로(5인치) 크기지정
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    colors = ['salmon', 'orange', 'cadetblue', 'skyblue']
    width = 0.15

    # 3. bar 그리기
    for i, model in enumerate(models):
        pos = compute_pos(xticks, width, i, models)
        if model == 'Multiprocess':
            bar = ax.bar(pos, data[model], width=width *
                         0.95, label=model, color=colors[i])
            hatch_str = "/"*4
            for bars in bar:
                bars.set_hatch(hatch_str)
        else:
            bar = ax.bar(pos, data[model], width=width *
                         0.95, label=model, color=colors[i])
        present_height(ax, bar)  # bar높이 출력

    # 4. x축 세부설정
    ax.set_xticks(range(len(xticks)))
    ax.set_xticklabels(xticks, fontsize=10)
    ax.set_xlabel('Number of thread/process', fontsize=14)

    # 5. y축 세부설정
    ax.set_ylim([0, 12])
    # ax.set_yticks([0.5, 0.55, 0.6, 0.65, 0.7, 0.75])
    ax.yaxis.set_tick_params(labelsize=10)
    ax.set_ylabel('Average detection time', fontsize=14)

    # 6. 범례 나타내기
    ax.legend(loc='upper left', shadow=True, ncol=1)

    # 7. 보조선(눈금선) 나타내기
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='gray', linestyle='dashed', linewidth=0.5)

    # 8. 그래프 저장하고 출력하기
    # plt.tight_layout()
    plt.savefig('ex_barplot.png', format='png', dpi=300)
    plt.show()


if __name__ == '__main__':
    main()
